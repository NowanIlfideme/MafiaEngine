from mafia_engine.base import GameObject

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
    pass


class Alignment(Entity):
    """Denotes an alignment (team), which might have properties of its own."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        pass
    pass


class Actor(Entity):
    """Denotes an actor entity (i.e. individual that can action)."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, roles
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        self.roles = kwargs.get("roles",[])

        pass
    pass

class Player(Actor):
    """Denotes an player entity (i.e. an actual, human player)."""

    def __init__(self, *args, **kwargs):
        """
        Keys: name, roles
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        pass

    pass
