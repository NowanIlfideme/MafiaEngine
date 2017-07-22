from mafia_engine.base import GameObject
from mafia_engine.ability.base import *

class EntityError(Exception): """Error with regards to entities."""

class Entity(GameObject):
    """Denotes a game-world entity."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        self.name = kwargs.get("name","")
        
        pass

    def __repr__(self):
        return "Entity."+ str(self.name)
    pass

class Moderator(Entity):
    """Denotes the moderator (usually just a listener)."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions ("event")
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        
        for event in kwargs.get("subscriptions",[]):
            self.engine.event_manager.subscribe(event,self)
            pass

        pass
    def __repr__(self):
        return "Mod."+ str(self.name)
    pass

class Alignment(Entity):
    """Denotes an alignment (team), which might have properties of its own."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        self.members = []
        pass
    
    def __repr__(self):
        return "Alignment."+ str(self.name)

    def add(self, actor):
        """Adds $actor to the alignment."""
        if not isinstance(actor, Actor):
            raise EntityError("Cannot add " + str(actor) + ", is not an Actor.")
        self.members.append(actor)
        if actor.alignment is None:
            actor.alignment = []
        actor.alignment.append(self)
        pass

    pass


class Actor(Entity):
    """Denotes an actor entity (i.e. individual that can action)."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, roles (list), alignment (list)
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        self.roles = kwargs.get("roles",[])
        self.alignment = kwargs.get("alignment",[])

        pass
    def __repr__(self):
        return "Actor."+ str(self.name)

    def action(self, *args, **kwargs):
        """
        Key: ability, target
        """

        actor = self
        
        ability = kwargs.get("ability","")
        #Find ability within roles
        found_roles = []
        for role in self.roles:
            if role.find_ability(ability) is not None:
                found_roles.append(role)
            pass
        if len(found_roles)==0:
            #Try to find disambiguation
            try:
                r_name, ability = _disambiguize(ability) #split into role and ability
                #Find role
                for R in self.roles:
                    if R.name==r_name:
                        found_roles.append(R)
            except: pass #len will still be 0
        if len(found_roles)!=1:
            raise AbilityError("Could not determine ability \
            exactly. Found roles: " + str(found_roles))

        target = kwargs.get("target","")

        found_roles[0].action(ability=ability, actor=actor, target=target)
        pass

    def get_abilities(self):
        res = []
        for r in self.roles:
            for a in r.abilities:
                res.append(a)
        return res

    def get_ability_names(self):
        return [a.name for a in self.get_abilities()]

    def _disambiguize(ability="."):
        """Breaks down ability into rolename and abilityname"""
        q = ability.split(".", maxsplit=1)
        return q[0], q[1]
    pass

class Player(Actor):
    """Denotes an player entity (i.e. an actual, human player)."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, roles, alignment
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        pass
    def __repr__(self):
        return "Player."+ str(self.name)

    pass


class Role(GameObject):
    """Denotes a game role, e.g. "mafioso" or "doctor".
    Roles consist of:
        - an Alignment (which determines WinCons (win conditions) and such);
        - Abilities (which are potential Actions);
        - Status
        - TODO: Other stuff (such as ActionPoint restrictions?)
    """
    
    def __init__(self, *args, **kwargs):
        """
        Keys: name, alignment, abilities, status
        """
        super().__init__(self, *args, **kwargs)
        #TODO Add local members.
        self.name = kwargs.get("name","")
        self.aligment = kwargs.get("alignment",None)
        self.abilities = kwargs.get("abilities",[]) # [Ability]
        self.status = kwargs.get("status",{})       # name : value

        pass

    def __repr__(self):
        return "Role."+ str(self.name)

    def action(self, *args, **kwargs):
        """
        Key: ability, actor, target
        """
        
        #TODO: Find ability within list, check if it's an ActivatedAbility.
        #If everything checks out, call it.

        ability = kwargs.get("ability","")
        found_abil = self.find_ability(ability)

        if not isinstance(found_abil, ActivatedAbility):
            raise AbilityError("Ability " + str(found_abil) + " is not an ActivatedAbility.")


        #TODO: Find actor, target.
        actor = kwargs.get("actor","")
        target = kwargs.get("target","")

        found_abil.action(ability=found_abil, actor=actor, target=target)
        pass

    def find_ability(self, ability=""):
        found_abil = None
        for a in self.abilities:
            if a.name==ability:
                found_abil=a
        return found_abil
        

    pass