import yaml, logging

def load_from_config(filename):
    """Reads and loads from a YAML config file."""
    #TODO: Add YAML-based config.
    pass

class GameObject(object):
    """Defines a game object. This helps in finding the object's environment 
    (i.e. the current game, symbolized by a GameEngine reference).
    Through that, it can find the EventManager, global logger, etc."""

    default_engine = None

    def __init__(self, *args, **kwargs):
        
        try:
            self.engine = kwargs["engine"]
        except:
            self.engine = self.default_engine
        return


    pass

class HistoryManager(object):
    """Saves all events in chronological and searchable order.
    TODO: Implement!
    """


    pass

class EventManager(object):
    """Manager for in-game events. Works as follows:
    Listeners subscribe to Events.
    Whenever someone wants to raise an event, they Signal it, and all listeners 
        for the event are Signal'd with the event name and params.
    Events get logged AND saved in the history.
    History allows one to resume a game from a particular state.
    """

    def __init__(self, *args, **kwargs):
        """
        Keys: listeners (dict), history (HistoryManager)
        """
        self.listeners = {}
        self.logger = logging.getLogger(__name__)  #normal Python logger
        self.history = HistoryManager()
        return

    def subscribe(self, event, listener): #I would like to subscribe to "bee facts"
        """Subscribe @listener to @event. It will be signal()'d with information when it happens."""
        self.listeners[event].append(listener)
        return

    def unsubscribe(self, event, listener): #please stop sending me bee facts
        """No longer get signal()'d with regards to @event."""
        self.listeners[event].remove(listener)
        return

    def signal(self, event, parameters, notes=""): #"bee facts" says: "male bees inherit genes only from their mothers"
        """Notify all subscribers of @event by calling signal(@event, @parameters)."""
        #TODO: Add history (with notes?)
        #TODO: Add logging (with notes?)
        
        for l in self.listeners[event]:
            try:
                l.signal(event,parameters)
            except:
                #TODO: Handle exception for "function not defined" and such.
                pass
        return

    pass


class GameEngine(object):
    """Defines a complete Mafia-like game."""

    def __init__(self, *args, **kwargs):
        """
        Keys: entities (list), status (dict), phases (generator/None)
        """
        self.event_manager = EventManager()
        self.logger = logging.getLogger(__name__)
        self.entities = kwargs.get("entities",[])
        self.status = kwargs.get("status",{})
        self.phases = kwargs.get("phases",None)
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
