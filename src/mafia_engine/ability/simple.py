from .base import Ability, ActivatedAbility, AutomaticAbility


class Vote(ActivatedAbility):
    """Ability that gets activated by an Entity.
    This (usually) generates an Action and Event when used."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Add data members

        #target restrictions, e.g. "can-self-target"
        #phase restrictions, e.g. "day" or "night"
        #number of uses, e.g. "X-shot", or "unlimited"
        #

        pass

    pass

class MKill(ActivatedAbility):
    """Ability that gets activated by an Entity.
    This (usually) generates an Action and Event when used."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Add data members

        #target restrictions, e.g. "can-self-target"
        #phase restrictions, e.g. "day" or "night"
        #number of uses, e.g. "X-shot", or "unlimited"
        #

        pass

    pass

