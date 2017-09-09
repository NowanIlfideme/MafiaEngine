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

    def test(self, action):
        """Cancels action if not allowed (e.g. not in phase)."""


        curr_phase = self.engine.status["phase"]
        found = (curr_phase in self.phases)
        
        ok = False
        if self.mode=="allow": ok = found
        elif self.mode=="ban": ok = not found
        if not ok: action.canceled = True
        pass

    
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
                         #extra subs to reset counter
                         subscriptions = [PhaseChangeEvent, 
                                          PostActionEvent(MKillAction())], 
                         phases=phases, mode=mode, **kwargs)
        self.alignment = alignment
        self.was_used = was_used
        pass

    def test(self, action):
        """Cancels action if not allowed."""
        if self.was_used:
            action.canceled = True
        pass

    def signal(self, event):
        super().signal(event) #Take care of PreActionEvent
        if isinstance(event,PhaseChangeEvent):
            self.was_used = False
        elif isinstance(event, PostActionEvent):
            action = event.action
            if isinstance(action, MKillAction):
                self.was_used = True
            else: pass
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
            elif inspect.isclass(tt) and issubclass(tt, GameObject):
                self.target_types.append(tt())
            pass
        
        self.mode = mode
        pass

    @property
    def _target_types(self):
        return [type(q) for q in self.target_types]

    def test(self, action):
        """Cancels action if not allowed (i.e. bad target)."""

        found = False
        for t in self._target_types:
            if isinstance(action.target, t):
                found = True
                break
        ok = False
        if self.mode=="allow": ok = found
        elif self.mode=="ban": ok =  not found
        if not ok: action.canceled = True
        pass

    
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
    """Signals that a player voted for another."""

    yaml_tag = u"!VoteAction"

    def __init__(self, actor=None, target=None, canceled=False):
        super().__init__(canceled=canceled)
        self.actor = actor
        self.target = target
        pass

    def _action(self):
        """Does nothing in iself! VoteTally picks up automatically."""
        pass

    def repr_map(self):
        res = super().repr_map()
        res.update({
            'actor':self.actor,
            'target':self.target,
            })
        return res
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

    def __init__(self, actor=None, target=None, canceled = False):
        super().__init__(canceled=canceled)
        self.actor = actor
        self.target = target
        pass

    def _action(self):
        """Just sends the requried events."""
        #self.send_signal(MKillEvent(actor=actor,target=target))
        self.send_signal(DeathEvent(target=self.target))
        pass

    def repr_map(self):
        res = super().repr_map()
        res.update({
            'actor':self.actor,
            'target':self.target,
            })
        return res

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

