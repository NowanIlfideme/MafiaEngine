from mafia_engine.base import *
from mafia_engine.ability import *
from mafia_engine.entity import Player, Alignment

from mafia_engine.basic.logic import *

#############
# Basic restrictions
#############

@yaml_object(Y)
class UseCountRestriction(AbilityRestriction):
    """Restriction on uses per phase and in total.
    None means there is no restriction, while 0 means not allowed.
    If a phase is not specified, it defaults to 0.
    """

    def __init__(self, name = "", allowed_total=None, allowed_per_phase={}, 
                 used_total=0, used_this_phase=0, **kwargs):
        super().__init__(name, **kwargs)
        self.allowed_total = allowed_total
        self.used_total = used_total
        self.allowed_per_phase = allowed_per_phase
        self.used_this_phase = used_this_phase

        self.subscribe(PostActionEvent(ChangePhaseAction())) #
        pass

    def repr_map(self):
        res = super().repr_map()
        res.update({
            "allowed_total":self.allowed_total,
            "allowed_per_phase":self.allowed_per_phase,
            "used_total":self.used_total,
            "used_this_phase":self.used_this_phase,
            })
        return res

    def signal(self, event):
        """Automatically subscribed to Pre- and
        PostActionEvent for relevant event.
        Also subscribed to PostActionEvent for ChangePhaseAction (to reset)."""

        if isinstance(event, PreActionEvent):
            action = event.action
            if action.canceled: return #Already canceled, no use in testing

            # Test if OK to continue. If not - cancel.
            ok = True
            if self.allowed_total is not None and self.used_total>=self.allowed_total: ok=False
            else:
                phase = self.engine.status.get("phase", None)
                allowed_this_phase = self.allowed_per_phase.get(phase, 0) 
                #Note: Default to 0 if not given, while None is unlimited
                if allowed_this_phase is None: ok = True
                elif self.used_this_phase >= allowed_this_phase: ok = False
            if not ok:
                action.canceled = True
            pass
        elif isinstance(event, PostActionEvent):
            action = event.action
            if isinstance(action, ChangePhaseAction):
                # Phase was changed, update internal stat.
                self.used_this_phase = 0
                pass
            else:
                #Our action was made, update internal state
                self.used_total += 1
                self.used_this_phase += 1
                pass
            pass
        pass
    pass


@yaml_object(Y)
class TargetRestriction(AbilityRestriction):
    """TODO: Implement."""

    def __init__(self, name = '', **kwargs):
        return super().__init__(name, **kwargs)

    def repr_map(self):
        return super().repr_map()

    def signal(self, event):
        return super().signal(event)

    pass

@yaml_object(Y)
class ActorStatusRestriction(AbilityRestriction):
    """TODO: Implement."""

    def __init__(self, name = '', **kwargs):
        return super().__init__(name, **kwargs)

    def repr_map(self):
        return super().repr_map()

    def signal(self, event):
        return super().signal(event)

    pass


#############
# Voting
#############

@yaml_object(Y)
class VoteAction(Action):
    """Adds a vote from $actor to $target on $tally."""

    def __init__(self, actor=None, target=None, tally=None, canceled = False, **kwargs):
        super().__init__(actor=actor, canceled=canceled, **kwargs)
        self.target = target
        self.tally = tally
        pass

    def repr_map(self):
        res=super().repr_map()
        res.update({
            'target':self.target,
            'tally':self.tally,
            })
        return res

    def _action(self):
        self.tally.add_vote(source=self.actor, target=self.target)
        pass

    pass

@yaml_object(Y)
class VoteAbility(ActivatedAbility):
    """Allows one to vote."""

    def __init__(self, restrictions = [], **kwargs):
        return super().__init__(restrictions=restrictions, **kwargs)

    def repr_map(self): return super().repr_map()

    @property
    def action_type(self): return VoteAction

    def action(self, actor=None, target=None, tally=None, **kwargs):
        return super().action(actor=None, target=None, tally=None, **kwargs)


    pass


#############
# Basic killing/murdering
#############

@yaml_object(Y)
class MurderAction(Action):
    """TODO: Implement."""

    def __init__(self, actor=None, target=None, canceled = False, **kwargs):
        super().__init__(actor=actor, canceled=canceled, **kwargs)
        self.target=target
        pass

    def repr_map(self):
        res=super().repr_map()
        res.update({
            'target':self.target,
            })
        return res

    def _action(self):
        super()._action()
        pass

    pass

@yaml_object(Y)
class MurderAbility(ActivatedAbility):
    """TODO: Implement."""

    def __init__(self, restrictions = [], **kwargs):
        return super().__init__(restrictions, **kwargs)

    def repr_map(self):
        return super().repr_map()

    def action(self, **kwargs):
        return super().action(**kwargs)

    @property
    def action_type(self):
        return super().action_type()

    pass


#############
# 
#############

@yaml_object(Y)
class _A(Action):
    """TODO: Implement."""

    def __init__(self, actor=None, target=None, canceled = False, **kwargs):
        super().__init__(actor=actor, canceled=canceled, **kwargs)
        self.target=target
        pass

    def repr_map(self):
        res=super().repr_map()
        res.update({
            'target':self.target,
            })
        return res

    def _action(self):
        super()._action()
        pass

    pass

@yaml_object(Y)
class __AA(ActivatedAbility):
    """TODO: Implement."""

    def __init__(self, restrictions = [], **kwargs):
        return super().__init__(restrictions, **kwargs)

    def repr_map(self):
        return super().repr_map()

    def action(self, **kwargs):
        return super().action(**kwargs)

    @property
    def action_type(self):
        return super().action_type()

    pass

