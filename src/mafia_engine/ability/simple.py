from .base import *
from ..entity import *

def DayNightGen(max_days=None):
    i = 0
    while (max_days==None or i<max_days):
        i += 1
        if i%2==0: yield "day"
        else: yield "night"
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
        if not isinstance(target, Actor):
            raise AbilityError(self.name + " failed on " + target.name + ": Not an Actor.")
            pass
        #TODO: Handle "no vote"/"unvote" case

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
            pass

        #TODO: Check if mafiakill has been used already! (via "status" of self.alignment)
        
        #TODO: Perform the kill!


        pass
    pass

