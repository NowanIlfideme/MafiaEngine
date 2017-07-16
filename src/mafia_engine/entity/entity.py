from mafia_engine.base import GameObject

class Entity(GameObject):
    """Denotes a game-world entity."""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        #TODO: Implement
        pass

    pass

class Alignment(Entity):
    """Denotes an alignment (team), which might have properties of its own."""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        #TODO: Implement
        pass

    pass

class Actor(Entity):
    """Denotes an actor entity (i.e. individual that can action)."""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        #TODO: Implement
        pass

    pass

