from mafia_engine.base import *
from mafia_engine.entity import *
from mafia_engine.preset.event.simple import *

@yaml_object(Y)
class TestMod(Moderator):
    """Example moderator. Handles game logic."""

    yaml_tag = u"!TestMod"

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.vote_tally = VoteTally()
        self.phase_iter = kwargs.get("phase_iter",PhaseIterator())
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
            "phase_iter":self.phase_iter,
            } )
        return res


    def signal(self, event):

        #Get info
        prefix = "-> "

        #TODO: Fix to actually work with new-style events!

        """
        if "target" in parameters:
            real_target = parameters["target"]
            try: target = real_target.name
            except: target = str(real_target)
        else: target = "<unknown>"

        if "actor" in parameters:
            real_actor = parameters["actor"]
            try: actor = real_actor.name
            except: actor = str(real_actor)
        else: actor = "<unknown>"

        if "alignment" in parameters:
            real_alignment = parameters["alignment"]
            try: alignment = real_alignment.name
            except: alignment = str(real_alignment)
        else: alignment = "<unknown>"            

        """

        #Get message

        #TODO: Change for the type!

        if isinstance(event, VoteEvent): 
            print(prefix + event.actor.name + " voted for " + event.target.name + "!")
            self.vote_tally.add_vote(event.actor, event.target)
            pass

        if isinstance(event, PhaseChangeEvent):
            print(prefix + "Phase changed, now: " + self.engine.status["phase"])
            pass

        if isinstance(event, MKillEvent): 
            print(prefix + event.actor.name + " used mkill on " + event.target.name + "!")
            pass

        if isinstance(event, DeathEvent):
            print(prefix + event.target.name + " died!")
            pass

        if isinstance(event, AlignmentEliminatedEvent):
            print(prefix + event.alignment.name + " was eliminated!")
            #TODO: Game-end behavior, for the simple game!
            tmp = self.engine.entity.members_by_type(Alignment, True)
            tmp.remove(event.alignment)
            print(prefix + tmp[0].name + " has won!")
            self.engine.status["finished"]=True
            pass

        pass
    pass

@yaml_object(Y)
class VoteTally(GameObject):
    """Holds the voting tally for the day."""
    
    yaml_tag = u"!VoteTally"

    def __init__(self, *args, **kwargs):
        """
        Keys: engine
        """
        super().__init__(self, *args, **kwargs)
        self.subscribe(PhaseChangeEvent)
        
        self.votes = {}
        self.voted = {}
        pass

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
        """Resets"""
        #TODO: Implement!

        self.votes = {}
        self.voted = {}

        pass
    
    def signal(self, event):
        if isinstance(event, PhaseChangeEvent) and event.previous=="day":
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

            print("Votes: " + votes_str)
            print("Total: " + voted_str)

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
class PhaseIterator(GameObject):
    """Iterates over the phases sequentially."""

    yaml_tag = u"!PhaseIterator"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, phases, repeat
        """
        super().__init__(self, *args, **kwargs)
        self.phases = kwargs.get("phases",[])
        self.repeat = kwargs.get("repeat",True)
        self.current = 0
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

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "phases=%r, " % self.phases
        res += "repeat=%r, " % self.repeat
        res += "current=%r" % self.current
        res += ")" 
        return res

    def __str__(self):
        return "PhaseIterator." + str(self.phases)

    pass

