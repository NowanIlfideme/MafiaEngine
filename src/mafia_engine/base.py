import yaml, logging
from copy import deepcopy, copy

def load_from_config(filename):
    """Reads and loads from a YAML config file."""
    #TODO: Add YAML-based config.
    pass

class SecretYamlObject(yaml.YAMLObject):
    """Helper class for YAML serialization.
    Source: https://stackoverflow.com/questions/22773612/how-can-i-ignore-a-member-when-serializing-an-object-with-pyyaml """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pass

    hidden_fields = []
    @classmethod
    def to_yaml(cls,dumper,data):
        new_data = copy(data)
        for item in cls.hidden_fields:
            if item in new_data.__dict__:
               del new_data.__dict__[item]
        res = dumper.represent_yaml_object(cls.yaml_tag, new_data, cls, flow_style=cls.yaml_flow_style)
        return res
    pass

class GameObject(SecretYamlObject):
    """Defines a game object. This helps in finding the object's environment 
    (i.e. the current game, symbolized by a GameEngine reference).
    Through that, it can find the EventManager, other GameObjects, etc."""

    yaml_tag = u"!GameObject"
    #hidden_fields = []
    default_engine = None

    def __init__(self, *args, **kwargs):
        """
        Keys: engine
        """
        self.engine = kwargs.get("engine", self.default_engine)
        
        return

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "engine=%r" % self.engine
        
        res += ")" 
        return res

    def signal(self, event, parameters, notes=""):
        """Signals $self that $event happened.
        Override this."""
        pass

    def send_signal(self, event, parameters, notes=""):
        """Signal the event manager that $event happened."""
        self.engine.event_manager.signal(event,parameters=parameters,notes=notes)

    def subscribe(self, event):
        """Subscribe $self (as listener) to $event."""
        self.engine.event_manager.subscribe(event,self)
        pass

    def unsubscribe(self, event):
        """Unsubscribe $self (as listener) from $event."""
        self.engine.event_manager.unsubscribe(event,self)
        pass

    pass

class HistoryManager(SecretYamlObject):
    """Saves all events in chronological and searchable order.
    TODO: Implement!
    """

    yaml_tag = u"!HistoryManager"
    #hidden_fields = []

    def __init__(self, *args, **kwargs):
        """
        Keys: <none>
        """
        pass

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += ")"
        return res

    def __str__(self):
        return "HistoryManager"

    def signal(self, event, parameters, notes=""):
        """Saves an event to history. TODO: Implement."""
        pass

    pass

class EventManager(SecretYamlObject):
    """Manager for in-game events. Works as follows:
    Listeners subscribe to Events.
    Whenever someone wants to raise an event, they Signal it, and all listeners 
        for the event are Signal'd with the event name and params.
    Events get logged AND saved in the history.
    History allows one to resume a game from a particular state.
    """

    yaml_tag = u"!EventManager"
    hidden_fields = ["logger"]

    def __init__(self, *args, **kwargs):
        """
        Keys: listeners (dict), history (HistoryManager)
        """
        self.listeners = {}
        self.logger = logging.getLogger(__name__)  #normal Python logger
        self.history = HistoryManager()
        return

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "listeners=%r, " % self.listeners
        res += "history=%r" % self.history
        res += ")" 
        return res

    def yaml(self):
        dct = self.__dict__
        if "loggr" in dct:
            del(dct["logger"])
        return yaml.dump(dct)
 
    @staticmethod
    def load(data):
        vals = yaml.safe_load(data)
        return EventManager(
            listeners = vals["listeners"],
            history = vals["history"],
            phase_iter = vals["phase_iter"]
            )


    def subscribe(self, event, listener): #I would like to subscribe to "bee facts"
        """Subscribe @listener to @event. It will be signal()'d with information when it happens."""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)
        self.logger.debug("Subscription to: "+str(event)+" by "+str(listener))
        return

    def unsubscribe(self, event, listener): #please stop sending me bee facts
        """No longer get signal()'d with regards to @event."""
        if event in self.listeners:
            self.listeners[event].remove(listener)
            if len(self.listeners[event])==0:
                del(self.listeners[event])
            self.logger.debug("Unsubscription from: "+str(event)+" by "+str(listener))
        return

    def signal(self, event, parameters, notes=""): #"bee facts" says: "male bees inherit genes only from their mothers"
        """Notify all subscribers of @event by calling signal(@event, @parameters)."""

        self.history.signal(event, parameters, notes)
        
        if event in self.listeners:
            self.logger.debug("Signaling " + str(len(self.listeners[event])) + " with " + str(event) + " : " + str(parameters))
            for l in self.listeners[event]:
                try:
                    l.signal(event,parameters)
                except:
                    self.logger.exception("Could not signal.")
        else:
            self.logger.debug("Event "+str(event)+" happened, but 0 listeners.")
        return

    pass


class PhaseIterator(GameObject):
    """Iterates over the phases."""

    yaml_tag = u"PhaseIterator"
    #hidden_fields = []

    def __init__(self, *args, **kwargs):
        """
        Keys: name, phases, repeat
        """
        super().__init__(self, *args, **kwargs)
        self.phases = kwargs.get("phases",[])
        self.repeat = kwargs.get("repeat",True)
        self.current = 0
        pass

    def __iter__(self): return self

    def __next__(self):
        if len(self.phases)==0: raise StopIteration
        if self.current >= len(self.phases):
            if not self.repeat: raise StopIteration
            self.current = 0
        res = self.phases[self.current]
        self.current += 1
        return res

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "phases=%r, " % self.phases
        res += "repeat=%r, " % self.repeat
        res += "current=%r" % self.current
        res += ")" 
        return res

    def __str__(self):
        return "PhaseIterator."



class GameEngine(SecretYamlObject):
    """Defines a complete Mafia-like game."""

    yaml_tag = u"!GameEngine"
    hidden_fields = ["logger"]

    def __init__(self, *args, **kwargs):
        """
        Keys: entities (list), status (dict), phase_iter (iterator)
        """
        self.logger = logging.getLogger(__name__)
        self.entities = kwargs.get("entities",[])
        self.status = kwargs.get("status",{})
        self.event_manager = EventManager()
        self.phase_iter = kwargs.get("phase_iter",PhaseIterator())
        
        return


    def __repr__(self):
        #res = "%s(" % (self.__class__.__name__, )
        #res += "entities=%r, " % self.entities
        #res += "status=%r, " % self.status
        #res += "phase_iter=%r" % self.phase_iter
        #res += ")" 
        return "GameEngine"

    def yaml(self):
        dct = self.__dict__
        if "logger" in dct:
            del(dct["logger"])
        return yaml.dump(dct)

    @staticmethod
    def load(data):
        vals = yaml.safe_load(data)
        return GameEngine(
            entities = vals["entities"],
            status = vals["status"],
            phase_iter = vals["phase_iter"]
            )

    @property
    def phase(self):
        return self.status["phase"]

    @phase.setter
    def phase(self, q):
        self.status["phase"] = q
        pass

    def next_phase(self):
        """Goes to next phase, and signals a 'phase_change'"""
        old_phase = self.phase
        self.phase = next(self.phase_iter)
        self.event_manager.signal(
            "phase_change",
            {"previous_phase":old_phase,"new_phase":self.phase}
            )
        pass

    def entity_by_lambda(self, lamb, always_list=False):
        """Gets entities for whom $lamb(e) is True"""
        found_ents = []
        for e in self.entities:
            if lamb(e):
                found_ents.append(e)
        if always_list or len(found_ents)>1: return found_ents
        if len(found_ents)==0: return None
        return found_ents[0] #len==1


    def entity_by_name(self, name, always_list=False):
        """Gets entities whose name is $name."""
        return self.entity_by_lambda(
            lambda e: e.name==name, 
            always_list)


    def entity_by_type(self, type, always_list=False):
        """Gets entities who are instances of $type."""
        return self.entity_by_lambda(
            lambda e: isinstance(e, type),
           always_list)
    

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
    TODO:
        status - how to control what goes on? hope callers do everything? :D
        ???

    """
    pass


