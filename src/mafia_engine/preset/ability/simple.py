from mafia_engine.base import *
from mafia_engine.ability import *
from mafia_engine.entity import *

@yaml_object(Y)
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

    
    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            "phases":self.phases,
            "mode":self.mode,
            } )
        return res

    pass

@yaml_object(Y)
class MKillPhaseRestriction(PhaseRestriction):
    """Restriction on use phase and once-per-phase."""
    
    yaml_tag = u"!MKillPhaseRestriction"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, alignment (Alignment), phases (list), mode="allow" (alt: "ban")
        """
        super().__init__(self, *args, **kwargs)
        self.alignment = kwargs.get("alignment",None)
        
        #setup special stuff
        self.engine.event.subscribe(PhaseChangeEvent,self)
        self.engine.event.subscribe(MKillEvent,self)
        self.used = False
        pass

    def __call__(self, abil, *args, **kwargs):
        """Returns True if ability is allowed."""

        sup_tst = super().__call__(abil, *args, **kwargs)
        if not sup_tst: return False

        #custom code below
        return not self.used

    def signal(self, event):
        if isinstance(event,PhaseChangeEvent):
            self.used = False
        elif isinstance(event, MKillEvent):
            self.used = True
        pass

    
    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            "alignment":self.alignment,
            "phases":self.phases,
            "mode":self.mode,
            } )
        return res

    pass

    
@yaml_object(Y)
class TargetRestriction(AbilityRestriction):
    """Restriction on target."""
    
    yaml_tag = u"!TargetRestriction"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, target_types (list of OBJECTS, default: [Entity()]), 
            mode="allow" (alt: "ban")
        """
        super().__init__(self, *args, **kwargs)
        self.target_types = kwargs.get("target_types",[Entity()])
        
        
        self.mode = kwargs.get("mode","allow")
        pass

    @property
    def _target_types(self):
        return [type(q) for q in self.target_types]

    def __call__(self, abil, *args, **kwargs):
        """Returns True if ability is allowed."""

        sup_tst = super().__call__(abil, *args, **kwargs)
        if not sup_tst: return False

        #custom code below
        target = kwargs.get("target",None)
        found = False
        try:
            for t in self._target_types:
                if isinstance(target, t):
                    found = True
                    break
        except Exception as e:
            raise AbilityError("TargetRestriction Error: " + str(e))
        if self.mode=="allow": return found
        elif self.mode=="ban": return not found
        return False

    
    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            "target_types":self.target_types, #NOTE: This might cause problems!
            "mode":self.mode,
            } )
        return res

    pass



@yaml_object(Y)
class VoteAction(Action):
    """Signals that a player voted for another.
    TODO: Implement a change to the VoteTally instead of doing it there!"""

    yaml_tag = u"!VoteAction"

    def action(self, *args, **kwargs):
        """Just sends a vote event."""
        self.engine.event.signal(
            VoteEvent(
                actor=kwargs.get("actor",None),
                target=kwargs.get("target",None),
                )
            )
        pass

    def repr_map(self):
        return super().repr_map()
    pass

@yaml_object(Y)
class VoteAbility(ActivatedAbility):
    """Classic vote "ability". Phase restriction set at "day" and "actor".
    TODO: Implement."""

    yaml_tag = u"!VoteAbility"

    @property
    def action_type(self):
        return VoteAction

    def __init__(self, *args, **kwargs):
        """
        Keys: name
        """
        #TODO: Add data members


        # Add base restrictions
        kwargs["restrictions"] = kwargs.get("restrictions",[])
        kwargs["restrictions"].extend(
            [
            PhaseRestriction(name="phase_r", phases=["day"]),
            TargetRestriction(name="target_r", target_types=[Actor()])
            ]
        )
        super().__init__(self, *args, **kwargs)


        #

        pass

    def action(self, *args, **kwargs):
        """
        Keys: actor, target
        """

        super().action(self, *args, **kwargs)
        pass
    pass

@yaml_object(Y)
class MKillAction(Action):
    """Does a mafia kill action.
    TODO: Implement actual action, not just events?"""
    
    yaml_tag = u"!MKillAction"

    def action(self, *args, **kwargs):
        """Just sends the requried events."""
        target = kwargs.get("target", None)
        actor = kwargs.get("actor", None)

        self.send_signal(MKillEvent(actor=actor,target=target))
        self.send_signal(DeathEvent(target=target))
        pass


@yaml_object(Y)
class MKillAbility(ActivatedAbility):
    """Classic mafiakill ability. Phase restriction set manually. Only one member can kill. 
    TODO: Implement."""

    yaml_tag = "!MKillAbility"

    @property
    def action_type(self):
        return MKillAction

    def __init__(self, *args, **kwargs):
        """
        Keys: name, alignment
        """

        # Add base restrictions
        m_align = kwargs.get("alignment", None)

        kwargs["restrictions"] = kwargs.get("restrictions",[])
        kwargs["restrictions"].extend(
            [
            MKillPhaseRestriction(name="mkill_phase_r", alignment=m_align, phases=["night"]),
            TargetRestriction(name="target_r", target_types=[Actor()]),
            ]
        )

        super().__init__(self, *args, **kwargs)

        pass

    def action(self, *args, **kwargs):
        """
        Keys: actor, target
        """
        super().action(self, *args, **kwargs)
        pass
    pass

