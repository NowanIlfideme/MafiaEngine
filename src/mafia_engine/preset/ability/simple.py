from mafia_engine.base import *
from mafia_engine.ability import *
from mafia_engine.entity import *

class Vote(ActivatedAbility):
    """Classic vote "ability". Phase restriction set manually.
    TODO: Implement."""

    yaml_tag = u"!Vote"

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

    yaml_tag = "!MKill"

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

