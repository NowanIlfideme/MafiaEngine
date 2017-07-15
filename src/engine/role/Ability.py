

class Ability(GameObject):
    """Denotes an ability, which can be used as an Action.
    This is a base type for Activated and Automatic abilities
    (akin to Magic: The Gathering's system). """

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)

        #TODO: Add data memebers

        pass

    pass

class ActivatedAbility(Ability):
    """Ability that gets activated by an Entity.
    This (usually) generates an Action and Event when used."""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        #TODO: Add data members

        #target restrictions, e.g. "can-self-target"
        #phase restrictions, e.g. "day" or "night"
        #number of uses, e.g. "X-shot", or "unlimited"
        #

        pass

    pass

class AutomaticAbility(Ability):
    """Ability that triggers from an Event.
    This might generate a new Action + Event."""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        #TODO: Add data members

        pass

    pass