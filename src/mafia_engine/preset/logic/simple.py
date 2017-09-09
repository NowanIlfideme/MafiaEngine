from mafia_engine.base import *
from mafia_engine.entity import *
from mafia_engine.preset.event.simple import *
from mafia_engine.preset.ability.simple import *

@yaml_object(Y)
class VoteTally(ProxyObject):
    """Holds the voting tally for the day."""
    
    yaml_tag = u"!VoteTally"

    def __init__(self, name="", votes={}, voted={}, **kwargs):
        subs = [PhaseChangeEvent(), PostActionEvent(VoteAction())]
        super().__init__(name=name, subscriptions=subs, **kwargs)        
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

    def lynch_result(self):
        """Get current result"""

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
    
    def signal(self, event):
        if isinstance(event, PostActionEvent):
            action = event.action
            if isinstance(action, VoteAction):

                pass
        elif isinstance(event, PhaseChangeEvent) and event.previous=="day":
            #Process votes!

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

            target = self.lynch_result()

            #Kill person (if None, then pass)
            if target is not None:
                self.send_signal(LynchEvent(target=target))
                target.status["dead"] = True
                self.send_signal(DeathEvent(target=target))
                pass

            #Reset voting
            self.reset()
            pass
        
        pass

    pass

@yaml_object(Y)
class TestMod(Moderator):
    """Example moderator. Handles game logic."""

    yaml_tag = u"!TestMod"

    def __init__(self, name="", vote_tally=None, phase_iter=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.vote_tally = VoteTally() if (vote_tally is None) else vote_tally
        self.phase_iter = PhaseIterator() if (phase_iter is None) else phase_iter
        pass

    def next_phase(self):
        """Goes to next phase, and signals a 'phase_change'"""

        old_phase = self.engine.status["phase"]
        new_phase = next(self.phase_iter)

        self.engine.status["phase"] = new_phase
        self.engine.event.signal(
            PhaseChangeEvent(previous=old_phase,current=new_phase)
            )

        pass

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            "vote_tally":self.vote_tally,
            "phase_iter":self.phase_iter,
            } )
        return res


    def signal(self, event):

        #Get info
        prefix = "-> "

        #Get message
        if isinstance(event, ActionEvent):
            action = event.action
            if isinstance(action, VoteAction):
                print("%s%s voted for %s!" % (prefix, action.actor.name, action.target.name) )
                self.vote_tally.add_vote(action.actor, action.target)
            elif isinstance(action, MKillAction):
                print("%s%s used mkill on %s!" % (prefix, action.actor.name, action.target.name) )
            else: pass
            pass


        if isinstance(event, PhaseChangeEvent):
            print("%sPhase changed, now: %s" % (prefix, self.engine.status["phase"]) )
            pass


        if isinstance(event, DeathEvent):
            print("%s%s died!" % (prefix, event.target.name) )
            pass

        if isinstance(event, AlignmentEliminatedEvent):
            print("%s%s was eliminated!" % (prefix, event.alignment.name) )
            #TODO: Game-end behavior, for the simple game!
            tmp = self.engine.entity.members_by_type(Alignment, True)
            tmp.remove(event.alignment)
            print("%s%s has won!" % (prefix, tmp[0].name) )
            self.engine.status["finished"]=True
            pass

        pass
    pass


@yaml_object(Y)
class PhaseIterator(GameObject):
    """Iterates over the phases sequentially."""

    yaml_tag = u"!PhaseIterator"

    def __init__(self, name="", phases=[], repeat=True, current=0, **kwargs):
        super().__init__(name=name, **kwargs)
        self.phases = phases
        self.repeat = repeat
        self.current = current
        pass

    def __iter__(self): return self

    def __next__(self):
        if len(self.phases)==0: raise StopIteration
        if self.current >= len(self.phases):
            if not self.repeat: raise StopIteration
            self.current = 0
        res = self.phases[self.current]
        self.current += 1
        return res

    def repr_map(self):
        res = super().repr_map()
        res.update( {
            "phases" : self.phases,
            "repeat" : self.repeat,
            "current" : self.current
            })
        return res
    pass

