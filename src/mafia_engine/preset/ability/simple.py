from mafia_engine.base import *
from mafia_engine.ability import *
from mafia_engine.entity import *


class PhaseRestriction(AbilityRestriction):
    """Restriction on use phase."""
    
    yaml_tag = u"!PhaseRestriction"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, phases (list), mode="allow" (alt: "ban")
        """
        super().__init__(self, *args, **kwargs)
        self.phases = kwargs.get("phases",[])
        self.mode = kwargs.get("mode","allow")
        pass

    def __call__(self, abil, *args, **kwargs):
        """Returns True if ability is allowed."""

        sup_tst = super().__call__(abil, *args, **kwargs)
        if not sup_tst: return False

        #custom code below
        curr_phase = self.engine.status["phase"]
        try:
            found = (curr_phase in self.phases)
            #other modes are 
        except Exception as e:
            raise AbilityError("PhaseRestriction Error: " + str(e))
        if self.mode=="allow": return found
        elif self.mode=="ban": return not found
        return False

    def __str__(self): return "PhaseRestriction."+ str(self.name)

    def __repr__(self):
        dct = { 
            "name": self.name, 
            "phases": self.phases, 
            "mode": self.mode, 
            "engine": self.engine
            }
        res = "%s(" % self.__class__.__name__
        res += ", ".join([q+"=%r" for q in dct]) % tuple([dct[q] for q in dct])
        res += ")" 
        return res
    pass


    
class TargetRestriction(AbilityRestriction):
    """Restriction on target."""
    
    yaml_tag = u"!TargetRestriction"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, target_types (list, default: [Entity]), 
            mode="allow" (alt: "ban")
        """
        super().__init__(self, *args, **kwargs)
        self.target_types = kwargs.get("target_types",[Entity])
        self.mode = kwargs.get("mode","allow")
        pass

    def __call__(self, abil, *args, **kwargs):
        """Returns True if ability is allowed."""

        sup_tst = super().__call__(abil, *args, **kwargs)
        if not sup_tst: return False

        #custom code below
        target = kwargs.get("target",None)
        found = False
        try:
            for t in self.target_types:
                if isinstance(target, t):
                    found = True
                    break
        except Exception as e:
            raise AbilityError("TargetRestriction Error: " + str(e))
        if self.mode=="allow": return found
        elif self.mode=="ban": return not found
        return False

    def __str__(self): return "TargetRestriction."+ str(self.name)

    def __repr__(self):
        dct = { 
            "name": self.name, 
            "target_types": self.target_types, 
            "mode": self.mode, 
            "engine": self.engine
            }
        res = "%s(" % self.__class__.__name__
        res += ", ".join([q+"=%r" for q in dct]) % tuple([dct[q] for q in dct])
        res += ")" 
        return res
    pass



    

class Vote(ActivatedAbility):
    """Classic vote "ability". Phase restriction set manually.
    TODO: Implement."""

    yaml_tag = u"!Vote"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, phase, total_uses, uses
        """
        #TODO: Add data members
        #target restrictions, e.g. "can-self-target"
        #phase restrictions, e.g. "day" or "night"
        #number of uses, e.g. "X-shot", or "unlimited"

        #TODO: Add restrictions here instead of in MafiaHelperUI

        super().__init__(self, *args, **kwargs)

        #

        pass

    def action(self, *args, **kwargs):
        """
        Keys: actor, target
        """
        super().action(self, *args, **kwargs)

        # NOTE: All that needs to be done is signal intent...
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

        #TODO: Add data members
        #target restrictions, e.g. "can-self-target"
        #phase restrictions, e.g. "day" or "night"
        #number of uses, e.g. "X-shot", or "unlimited"
        #

        #TODO: Add restrictions here instead of in MafiaHelperUI

        super().__init__(self, *args, **kwargs)

        pass

    def action(self, *args, **kwargs):
        """
        Keys: actor, target
        """
        super().action(self, *args, **kwargs)

        target = kwargs.get("target", None)
        actor = kwargs.get("actor", None)

        #TODO: Move to Restriction!
        #Check if mafiakill has been used already! (via "status" of self.alignment)
        mkill_used = False
        if actor.alignment[0].status.get("mkill_used", False): 
            mkill_used = True
        if mkill_used:
            raise AbilityError(self.name + " failed: already used!")


        #Perform the kill!
        actor.alignment[0].status["mkill_used"] = True
        target.status["dead"] = True
        self.send_signal("death", parameters = { "target":target } )


        pass
    pass

