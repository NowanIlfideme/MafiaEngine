import yaml, logging
from mafia_engine.EventManager import EventManager

class GameEngine(object):
    """Defines a complete Mafia-like game."""
    def __init__(self):
        self.event_manager = EventManager()
        self.logger = logging.getLogger(__name__)
        self.entities = []
        self.status = {}
        return

    def load(self,filename):
        """Loads an existing game from a file."""
        #TODO: Implement loading from file.
        return self

    def load(filename):
        """Loads an existing game from a file."""
        #TODO: Implement loading from file.
        obj = GameEngine()
        return obj

    def clone(other):
        """Creates a copy of game "other"."""
        #TODO: Implement copying
        obj = GameEngine()
        return obj

    def clone(self):
        """Creates a copy of self."""
        #TODO: Implement copying
        obj = GameEngine()
        return obj

    """
    TODO: Lots of stuff!
        phases - how to handle? options:
            - as a ("day", "night") thing
            - as a generator (so that non-cyclic things can be used)
            - ???
        status - how to control what goes on? hope callers do everything? :D
        ???

    """
    pass