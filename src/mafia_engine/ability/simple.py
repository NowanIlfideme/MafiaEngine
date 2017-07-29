from .base import *
from ..entity import *

#Not actually used, but w/e?
def DayNightGen(max_days=None):
    i = 0
    while (max_days==None or i<max_days):
        i += 1
        if i%2==0: yield "day"
        else: yield "night"
    yield None
    pass


class Vote(ActivatedAbility):
    """Classic vote "ability". Phase restriction set manually.
    TODO: Implement."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, phase, total_uses, uses
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Add data members

        #target restrictions, e.g. "can-self-target"
        #phase restrictions, e.g. "day" or "night"
        #number of uses, e.g. "X-shot", or "unlimited"
        #

        pass

    def action(self, *args, **kwargs):
        """
        Keys: actor, target
        """
        super().action(self, *args, **kwargs)

        #Check if target is an Actor, or None
        target = kwargs.get("target", None)
        if not (isinstance(target, Actor) or target is None):
            raise AbilityError(self.name + " failed on " + target.name + ": Not an Actor or None.")
            pass

        pass
    pass

class MKill(ActivatedAbility):
    """Classic mafiakill ability. Phase restriction set manually. Only one member can kill. 
    TODO: Implement."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, phase, total_uses, uses
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Add data members

        #target restrictions, e.g. "can-self-target"
        #phase restrictions, e.g. "day" or "night"
        #number of uses, e.g. "X-shot", or "unlimited"
        #

        pass

    def action(self, *args, **kwargs):
        """
        Keys: actor, target
        """
        super().action(self, *args, **kwargs)

        target = kwargs.get("target", None)
        actor = kwargs.get("actor", None)

        #Check if target is an Actor
        if not isinstance(target, Actor):
            raise AbilityError(self.name + " failed on " + target.name + ": Not an Actor.")


        #Check if mafiakill has been used already! (via "status" of self.alignment)
        mkill_used = False
        if actor.alignment[0].status.get("mkill_used", False): 
            mkill_used = True

        if mkill_used:
            raise AbilityError(self.name + " failed: already used!")

        #Check for other circumstances (e.g. protection or immunity)


        #Perform the kill!
        actor.alignment[0].status["mkill_used"] = True
        target.status["dead"] = True
        self.send_signal("death", parameters = { "target":target } )


        pass
    pass

class MafiaAlignment(Alignment):
    """Denotes the mafia team."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions (list), status (dict)
        """

        if "subscriptions" in kwargs:
            if "phase_change" not in kwargs["subscriptions"]:
                kwargs["subscriptions"].append("phase_change")
        else: kwargs["subscriptions"] = ["phase_change"]

        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        pass
    
    def signal(self, event, parameters, notes=""):
        super().signal(event, parameters, notes)

        if event=="phase_change":
            self.status["mkill_used"] = False
            pass

        pass

    pass


class VoteTally(GameObject):
    """Holds the voting tally for the day."""

    def __init__(self, *args, **kwargs):
        """
        Keys: engine
        """
        super().__init__(self, *args, **kwargs)
        self.subscribe("phase_change")
        
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
    
    def signal(self, event, parameters, notes=""):
        if event=="phase_change" and parameters["previous_phase"]=="day":
            #Process votes!
            print("Votes: " + str(self.votes))
            print("Total: " + str(self.voted))

            target = self.lynch_result()

            #Kill person (if None, then pass)
            if target is not None:
                self.send_signal("lynch", parameters = { "target":target })
                target.status["dead"] = True
                self.send_signal("death", parameters = { "target":target } )
                pass

            #Reset voting
            self.reset()
            pass
        pass

    pass

class TestMod(Moderator):
    """Example moderator."""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.vote_tally = VoteTally()
        pass

    def signal(self, event, parameters, notes=""):

        #Get info
        prefix = "-> "

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

        #Get message

        if event=="": pass

        if event=="vote":
            print(prefix + actor + " voted for " + target + "!")
            self.vote_tally.add_vote(real_actor, real_target)
            pass

        if event=="phase_change":
            print(prefix + "Phase changed, now: " + self.engine.phase)
            pass

        if event=="mkill": 
            print(prefix + actor + " mkilled " + target + "!")
            pass

        if event=="death":
            print(prefix + target + " died!")
            pass

        if event=="alignment_eliminated":
            print(prefix + alignment + " was eliminated!")
            #TODO: Game-end behavior, for the simple game!
            tmp = self.engine.entity_by_type(Alignment,True)
            tmp.remove(parameters["alignment"])
            print(prefix + tmp[0].name + " has won!")
            self.engine.status["finished"]=True
            pass

        pass