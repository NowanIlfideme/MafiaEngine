from mafia_engine.base import *
from mafia_engine.ability import *
from mafia_engine.entity import *

@yaml_object(Y)
class PhaseRestriction(AbilityRestriction):
    """Restriction on use phase.
    mode: 'allow' or 'ban'."""
    
    yaml_tag = u"!PhaseRestriction"

    def __init__(self, name="", phases=[], mode="allow", **kwargs):
        super().__init__(name=name, **kwargs)
        self.phases = phases
        self.mode = mode
        pass

    def __call__(self, abil, **kwargs):
        """Returns True if ability is allowed."""

        sup_tst = super().__call__(abil, **kwargs)
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
    """Restriction on use phase and once-per-phase.
    mode: 'allow' or 'ban'."""
    
    yaml_tag = u"!MKillPhaseRestriction"

    def __init__(self, name="", alignment=None, phases=[], mode="allow", 
                    was_used = False, **kwargs):
        super().__init__(name=name, 
                         subscriptions = [PhaseChangeEvent, MKillEvent],
                         phases=phases, mode=mode, **kwargs)
        self.alignment = alignment
        self.was_used = was_used
        pass

    def __call__(self, abil, **kwargs):
        """Returns True if ability is allowed."""

        sup_tst = super().__call__(abil, **kwargs)
        if not sup_tst: return False

        #custom code below
        return not self.was_used

    def signal(self, event):
        if isinstance(event,PhaseChangeEvent):
            self.was_used = False
        elif isinstance(event, MKillEvent):
            self.was_used = True
        pass

    
    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            "alignment":self.alignment,
            "phases":self.phases,
            "mode":self.mode,
            "was_used":self.was_used,
            } )
        return res

    pass

    
@yaml_object(Y)
class TargetRestriction(AbilityRestriction):
    """Restriction on target.
    mode: 'allow' or 'ban'."""
    
    yaml_tag = u"!TargetRestriction"

    def __init__(self, name="", target_types=[Entity], mode="allow", **kwargs):
        super().__init__(name="", **kwargs)

        self.target_types = []
        for tt in target_types:
            if isinstance(tt, GameObject):
                self.target_types.append(tt)
            elif issubclass(tt, GameObject):
                self.target_types.append(tt())
            pass
        
        self.mode = mode
        pass

    @property
    def _target_types(self):
        return [type(q) for q in self.target_types]

    def __call__(self, abil, target=None, **kwargs):
        """Returns True if ability is allowed."""

        sup_tst = super().__call__(abil, target=target, **kwargs)
        if not sup_tst: return False

        #custom code below
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
            "target_types":self.target_types,
            "mode":self.mode,
            } )
        return res

    pass



@yaml_object(Y)
class VoteAction(Action):
    """Signals that a player voted for another.
    TODO: Implement a change to the VoteTally instead of doing it there!"""

    yaml_tag = u"!VoteAction"

    def action(self, actor=None, target=None, **kwargs):
        """Just sends a vote event."""
        self.engine.event.signal(
            VoteEvent(
                actor=actor,
                target=target,
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

    def __init__(self, name="", **kwargs):
        """
        Keys: name
        """
        # Add base restrictions
        restrictions = [
            PhaseRestriction(name="phase_r", phases=["day"]),
            TargetRestriction(name="target_r", target_types=[Actor])
        ]
        super().__init__(name=name, restrictions=restrictions, **kwargs)
        pass

    def action(self, actor=None, target=None, **kwargs):
        super().action(actor=actor, target=target, **kwargs)
        pass
    pass

@yaml_object(Y)
class MKillAction(Action):
    """Does a mafia kill action. (Really, just sends events)."""
    
    yaml_tag = u"!MKillAction"

    def action(self, actor=None, target=None, **kwargs):
        """Just sends the requried events."""
        self.send_signal(MKillEvent(actor=actor,target=target))
        self.send_signal(DeathEvent(target=target))
        pass


@yaml_object(Y)
class MKillAbility(ActivatedAbility):
    """Classic mafiakill ability. Phase restriction set manually. 
    Only one member can kill. """

    yaml_tag = "!MKillAbility"

    @property
    def action_type(self):
        return MKillAction

    def __init__(self, name="", alignment=None, **kwargs):
        # Add base restrictions
        restrictions= [
            MKillPhaseRestriction(name="mkill_phase_r", alignment=alignment,
                                 phases=["night"]),
            TargetRestriction(name="target_r", target_types=[Actor]),
        ]
        super().__init__(name=name, restrictions=restrictions, **kwargs)
        pass

    def action(self, actor=None, target=None,**kwargs):
        super().action(actor=actor, target=target, **kwargs)
        pass
    pass

