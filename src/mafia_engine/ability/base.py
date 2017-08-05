from mafia_engine.base import GameObject

class AbilityError(Exception): """Something wrong with an ability."""

class Ability(GameObject):
    """Denotes an ability, which can be used as an Action.
    This is a base type for Activated and Automatic abilities
    (akin to Magic: The Gathering's system). """

    def __init__(self, *args, **kwargs):
        """
        Keys: name
        """
        super().__init__(self, *args, **kwargs)
        self.name = kwargs.get("name","")
        #TODO: Add data memebers

        pass

    def __str__(self):
        return "Ability."+ str(self.name)

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "name=%r, " % self.name
        res += "engine=%r" % self.engine        
        res += ")"
        return res


    pass

class ActivatedAbility(Ability):
    """Ability that gets activated by an Entity.
    This (usually) generates an Action and Event when used."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, phase, total_uses, uses
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Add data members

        #target restrictions, e.g. "can-self-target"
        
        #phase restrictions, e.g. "day" or "night"
        self.phase = kwargs.get("phase", None) # none means any

        #number of uses, e.g. "X-shot", or "unlimited"
        self.total_uses = kwargs.get("total_uses", None) #none means infinite
        self.uses = kwargs.get("uses", self.total_uses) #default is max
        #

        pass

    def action(self, *args, **kwargs):
        """
        Keys: actor, target
        """
        #Check phase
        if self.phase is not None:
            if self.phase.count(self.engine.phase)==0:
                raise AbilityError(self.name + " cannot be used in phase " + str(self.engine.phase))
            pass

        #Check num of uses
        #TODO: !

        target = kwargs.get("target", None)
        actor = kwargs.get("actor", None)

        self.send_signal(self.name,
                         parameters = {
                             "actor":actor,
                             "target":target}
                         )
        pass

    def __str__(self):
        return "ActivatedAbility." + str(self.name)

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "name=%r, " % self.name
        res += "phase=%r, " % self.phase
        res += "total_uses=%r, " % self.total_uses
        res += "engine=%r" % self.engine
        res += ")"
        return res


    pass

class AutomaticAbility(Ability):
    """Ability that triggers from an Event.
    This might generate a new Action + Event."""

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        """
        Keys: name
        """
        #TODO: Add data members

        pass

    def __str__(self):
        return "AutomaticAbility." + str(self.name)

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "name=%r, " % self.name
        res += "engine=%r" % self.engine
        res += ")"
        return res

    pass