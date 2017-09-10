from mafia_engine.base import *
from mafia_engine.ability import *
from mafia_engine.entity import Player, Alignment

##############
#
##############


##############
# Game engine logic
##############





##############
# Phases
##############

@yaml_object(Y)
class ChangePhaseAction(Action):
    """Requests a phase change from a given PhaseChanger.
    Note that this can be interrupted (e.g. canceled or target phase changed)."""
    yaml_tag = u"!ChangePhaseAction"

    def __init__(self, actor = None, next_idx=None, phase_changer=None, canceled = False, **kwargs):
        super().__init__(actor, canceled, **kwargs)
        self.phase_changer = phase_changer
        self.next_idx = next_idx
        pass

    def _action(self):
        self.phase_changer.current_idx = self.next_idx
        pass

    pass

@yaml_object(Y)
class PhaseChanger(ProxyObject):
    """Iterates over the phases sequentially."""

    yaml_tag = u"!PhaseChanger"

    def __init__(self, name="", phases=[], current_idx=0, **kwargs):
        super().__init__(name=name, **kwargs)
        if len(phases)==0: raise ValueError("No phases given!")
        self.phases = phases
        self.current_idx = current_idx
        pass

    def repr_map(self):
        res = super().repr_map()
        res.update( {
            "phases" : self.phases,
            "current_idx" : self.current_idx,
            })
        return res

    @property
    def current(self): return self.phases[self.current_idx]

    def next_phase(self):
        new_idx = self.current_idx + 1
        if new_idx >= len(self.phases): new_idx = 0        
        cpa = ChangePhaseAction(actor=self, next_idx=new_idx, phase_changer=self)
        cpa.run()
        return self.current

    pass

#




##############
# Voting
##############

@yaml_object(Y)
class VoteTally(ProxyObject):
    """Holds a voting tally."""
    
    yaml_tag = u"!VoteTally"

    def __init__(self, name="", votes={}, voted={}, **kwargs):
        super().__init__(name=name, **kwargs)
        self.votes = votes
        self.voted = voted
        pass

    def repr_map(self):
        res = super().repr_map()
        res.update( {
            "votes":self.votes,
            "voted":self.voted,
            } )
        return res

    def add_vote(self, source, target):
        """Changes $source's vote to $target."""

        if self.votes.get(source, None)==target:
            return # Don't need to change a thing.
        self.votes[source] = target

        qty = self.voted.get(target, 0)
        self.voted[target] = qty + 1
        pass

    def result(self, do_print=True):
        """Get current result"""

        if do_print:
            #votes_str = str(self.votes)
            votes_str = "{"
            for k in self.votes:
                votes_str += str(k) + "->" + str(self.votes[k]) + ", "
            votes_str += "}"

            #voted_str = str(self.voted)
            voted_str = "{"
            for k in self.voted:
                voted_str += str(k) + ":" + str(self.voted[k]) + ", "
            voted_str += "}"

            res = "Votes: " + votes_str + "\n" + "Total: " + voted_str
            print(res)
            pass

        max_votes = 0
        maxed = []

        for t in self.voted:
            v = self.voted[t]
            if v>max_votes:
                maxed = [t]
                max_votes = v
            elif v==max_votes:
                maxed.append(t)
            pass

        if len(maxed)==1: return maxed[0]
        #in case of tie, no lynch
        return None

    def reset(self):
        """Resets all votes."""

        self.votes = {}
        self.voted = {}
        pass

    def process(self, do_print=True):
        """Processes votes, then resets. Override!"""

        target = self.result()
        # Run own action here

        self.reset()
        pass

    pass


@yaml_object(Y)
class LynchAction(Action):
    """Performs a lynch of a player.
    Note that this can be interrupted (e.g. canceled or target phase changed)."""
    yaml_tag = u"!LynchAction"

    def __init__(self, actor = None, target=None, tally=None, canceled = False, **kwargs):
        super().__init__(actor, canceled, **kwargs)
        self.target = target
        self.tally = tally
        pass

    def _action(self):
        if target is None: return
        
        # TODO: Turn into "kill code".
        target.status["dead"] = True
        pass

    pass


@yaml_object(Y)
class LynchVoteTally(VoteTally):
    """Holds vote tally for lynching."""

    def __init__(self, name = "", votes = {}, voted = {}, **kwargs):
        super().__init__(name, votes, voted, **kwargs)
        pass

    def process(self, do_print=True):
        """Processes votes, performs lynch, then resets."""

        #Lynch person (Note: target can be None!)
        target = self.result()
        l_act = LynchAction(actor=None, target=target, tally=self)
        l_act.run()

        self.reset()
        pass

    pass

