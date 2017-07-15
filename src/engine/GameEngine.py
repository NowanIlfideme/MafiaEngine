import yaml, logging


class GameEngine(object):
    """Defines a complete Mafia-like game."""
    def __init__(self):
        self.event_manager = EventManager()
        self.logger = logging.getLogger(__name__)
        self.entities = []
        return self

    def load(self,filename):
        """Loads an existing game from a file."""
        #TODO: Implement loading from file.
        return self

    def load(filename):
        """Loads an existing game from a file."""
        #TODO: Implement loading from file.
        obj = GameEngine()
        return obj

    """
    TODO: Lots of stuff!
        phases - how to handle? options:
            - as a ("day", "night") thing
            - as a generator (so that non-cyclic things can be used)
            - ???
        status - how to always keep reference to current game? options:
            - define base class (GameObject) that keeps 
                a reference to its GameEngine (-> logging and events)
                (I like this idea and will probably implement it...);
            - manually keep GameEngine reference, and do logging & hist
                in the EventManager()
            - always pass the current GameEngine (seems really dumb)
        ???


    """
    pass