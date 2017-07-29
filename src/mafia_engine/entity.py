from mafia_engine.base import GameObject
from mafia_engine.ability.base import *

class EntityError(Exception): """Error with regards to entities."""

class Entity(GameObject):
    """Denotes a game-world entity."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions (list), status (dict)
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        self.name = kwargs.get("name","")
        for event in kwargs.get("subscriptions",[]):
            self.subscribe(event)
            pass
        self.status = kwargs.get("status",{})
        pass

    def __repr__(self):
        return "Entity."+ str(self.name)
    pass


class Moderator(Entity):
    """Denotes the moderator (usually just a listener)."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions (list), status (dict)
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        
        

        pass
    def __repr__(self):
        return "Mod."+ str(self.name)
    pass


class Alignment(Entity):
    """Denotes an alignment (team), which might have properties of its own."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions (list), status (dict)
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
        Keys: name, subscriptions (list), roles (list)
        """
        #Pre-processing
        if "subscriptions" in kwargs:
            if "death" in kwargs["subscriptions"]:
                kwargs["subscriptions"].append("death")
        else: kwargs["subscriptions"] = ["death"]
        
        super().__init__(self, *args, **kwargs)
        
        #TODO: Implement
        self.roles = kwargs.get("roles",[])
        #self.__alignment = []
        self.status = {}
        
        pass

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

    def __repr__(self):
        return "Actor."+ str(self.name)

    def signal(self, event, parameters, notes=""):
        """Gets called on death and, possibly, other events."""

        #TODO: Handle death gracefully by... removing ones self from the game.
        #(as basic behavior - can be overridden, I guess)
        if event=="death":
            if parameters["target"]==self:
                if self in self.engine.entities:
                    self.engine.entities.remove(self)

        pass

    def action(self, *args, **kwargs):
        """Performs an action, specified by the name
        Key: ability, <ability args>
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

        kwargs["ability"]=ability
        #Below are things the "role" figures out by itself
        #target = kwargs.get("target","")
        found_roles[0].action(actor=actor, **kwargs)
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
    """Denotes an player actor (i.e. an actual, human player)."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions, roles, alignment
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement player-specific stuff
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
        self.alignment = kwargs.get("alignment",None)
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