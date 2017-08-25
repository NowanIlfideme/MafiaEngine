from mafia_engine.base import GameObject, Entity, Y, EntityError
from mafia_engine.ability import *
from mafia_engine.preset.event.simple import *

from ruamel.yaml import YAML, yaml_object


@yaml_object(Y)
class Moderator(Entity):
    """Denotes the moderator (the main input point for game logic). Base class."""

    yaml_tag = u"!Moderator"

    def __init__(self, name="", subscriptions=[], status={}, **kwargs):
        # No members!
        super().__init__(name=name, subscriptions=subscriptions,
                         status=status, members = [], **kwargs)
        pass

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            
            } )
        return res

    pass

@yaml_object(Y)
class Alignment(Entity):
    """Denotes an alignment (team), which might have properties of its own."""
    # NOTE: Inherit and override for each alignment.

    yaml_tag = u"!Alignment"

    def __init__(self, name="", subscriptions=[], status={},
                members=[], **kwargs):
        """
        Keys: name, subscriptions (list), status (dict), members (list)
        """
        super().__init__(name=name,subscriptions=subscriptions,
                        status=status, members=members, **kwargs)
        pass
    
    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            
            } )
        return res

    pass

@yaml_object(Y)
class Actor(Entity):
    """Denotes an actor entity (i.e. individual that can action). Base class."""
    # NOTE: Inherit and override for each actor.

    yaml_tag = u"!Actor"

    def __init__(self, name="", subscriptions=[], members=[], status={}, **kwargs):
        subs = subscriptions.copy()
        if DeathEvent not in subs:
            subs.append(DeathEvent) # Subscribe to own death, maybe?
        super().__init__(name=name, subscriptions=subs,
                         members=members, status=status, **kwargs)
        
        pass
    
    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            
            } )
        return res

    #TODO: Remake to search for alignment in tree.
    @property
    def alignment(self):
        #TODO: return alignments from roles
        try: r_aligns = [R.alignment for R in self.roles]
        except: r_aligns = []
        try: s_aligns = self.__alignment
        except: s_aligns = []
        aligns = s_aligns.copy()
        aligns.extend(r_aligns)
        res = set(aligns)
        
        #if len(res)==0: return None
        #if len(res)==1: return res.pop()
        return list(res)

    @alignment.setter
    def alignment(self, val):
        res = set(val) - set([R.alignment for R in self.roles])
        self.__alignment = list(res)


    def signal(self, event):
        """Gets called on death and, possibly, other events."""

        #New behavior: Set own "dead" as True
        if isinstance(event, DeathEvent):
            if event.target==self:
                self.status["dead"] = True

        #Old behavior: Handle death gracefully by... removing ones self from the game.
        #(as basic behavior - can be overridden, I guess)
        #if isinstance(event,DeathEvent):
        #    if event.target==self:
        #        self.engine.entity.remove(self) #needs to be redone           
        pass

    def action(self, ability="", actor=None, **kwargs):
        """Performs an action, specified by the name
        Key: ability, <ability args>
        """

        abil_name = ability

        found_abils = self.members_by_name(abil_name, True)
        found_abils = [a for a in found_abils if isinstance(a, ActivatedAbility)]

        if len(found_abils)!=1:
            raise AbilityError("Could not determine ability \
            exactly. Found: " + str(found_abils))
        fa = found_abils[0]

        if actor is None: actor=self
        fa.action(actor=actor, **kwargs)

        pass

    def get_ability_names(self):
        lamb = lambda x : isinstance(x,Ability)
        return [a.name for a in self.members_by_lambda(lamb,True)]

    def _disambiguize(ability="."):
        """Breaks down ability into rolename and abilityname"""
        q = ability.split(".", maxsplit=1)
        return q[0], q[1]
    pass

@yaml_object(Y)
class Player(Actor):
    """Denotes an player actor (i.e. an actual, human player)."""
    # NOTE: Inherit and override for each player.

    yaml_tag = u"!Player"

    def __init__(self, name="", subscriptions=[], status={}, members=[], **kwargs):
        """
        Keys: name, subscriptions, roles, alignment
        """
        super().__init__(name=name, subscriptions=subscriptions,
                         status=status, members=members, **kwargs)
        #TODO: Implement player-specific stuff
        pass

    
    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            
            } )
        return res

    pass

