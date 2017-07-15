
class GameObject(object):
    """Defines a game object. This helps in finding the object's environment 
    (i.e. the current game, symbolized by a GameEngine reference).
    Through that, it can find the EventManager, global logger, etc."""

    def __init__(self, engine):
        this.engine = engine
        return


    pass