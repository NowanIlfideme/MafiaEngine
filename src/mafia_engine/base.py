import yaml, logging
from copy import deepcopy, copy


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

    #@classmethod
    #def from_yaml(cls, loader, node):
    #    # ...
    #    data = super().from_yaml(loader,node)
    #    data.logger = logging.getLogger(__name__)
    #    return data

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
        Keys: engine, name
        """
        self.engine = kwargs.get("engine", self.default_engine)
        self.name = kwargs.get("name","")

        return

    def __str__(self): return "<GameObject.%s>" % self.name

    def __repr__(self):
        res = "%s(" % self.__class__.__name__
        res += "name=%r, " % self.name
        res += "engine=%r" % self.engine
        res += ")" 
        return res

    def signal(self, event, parameters, notes=""):
        """Signals $self that $event happened.
        Override this."""
        pass

    def send_signal(self, event, parameters, notes=""):
        """Signal the event manager that $event happened."""
        self.engine.event.signal(event,parameters,notes=notes)

    def subscribe(self, event):
        """Subscribe $self (as listener) to $event."""
        self.engine.event.subscribe(event,self)
        pass

    def unsubscribe(self, event):
        """Unsubscribe $self (as listener) from $event."""
        self.engine.event.unsubscribe(event,self)
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

    def __str__(self): return "HistoryManager"

    def __repr__(self):
        res = "%s(" % self.__class__.__name__
        res += ")"
        return res

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

    def __setstate__(self, kw): # For (de)serialization
        """
        Keys: listeners (dict), history (HistoryManager)
        """
        self.logger = logging.getLogger(__name__)  #normal Python logger
        self.listeners = kw.get("listeners",{})
        self.history = kw.get("history",HistoryManager())
        return

    def __init__(self, *args, **kwargs):
        """
        Keys: listeners (dict), history (HistoryManager)
        """
        self.__setstate__(kwargs)
        return

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "listeners=%r, " % self.listeners
        res += "history=%r" % self.history
        res += ")" 
        return res

    def subscribe(self, event, listener): 
        """Subscribe @listener to @event. It will be signal()'d with information when it happens."""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)
        self.logger.debug("Subscription to: "+str(event)+" by "+str(listener))
        return

    def unsubscribe(self, event, listener): 
        """No longer get signal()'d with regards to @event."""
        if event in self.listeners:
            self.listeners[event].remove(listener)
            if len(self.listeners[event])==0:
                del(self.listeners[event])
            self.logger.debug("Unsubscription from: "+str(event)+" by "+str(listener))
        return

    def signal(self, event, parameters, notes=""): 
        """Notify all subscribers of @event by calling signal(@event, @parameters)."""

        self.history.signal(event, parameters, notes)
        
        if event in self.listeners:
            par_str = "{" + "".join([str(key) + " : " + str(parameters[key]) + ", " for key in parameters])[:-2] + "}"
            #Instead of str(parameters), which gives the __repr__ of the param values...
            #The "[:-2]" is for removing the trailing ", ". On an empty string, it doesn't matter.

            self.logger.debug("Signaling " + str(len(self.listeners[event])) + " with " + str(event) + " : " + par_str)
            for l in self.listeners[event]:
                try:
                    l.signal(event,parameters)
                except:
                    self.logger.exception("Could not signal.")
        else:
            self.logger.debug("Event "+str(event)+" happened, but 0 listeners.")
        return

    pass



class GameEngine(SecretYamlObject):
    """Defines a complete Mafia-like game."""

    yaml_tag = u"!GameEngine"
    #hidden_fields = ["logger"]

    def __init__(self, *args, **kwargs):
        """
        Keys: entities (list), status (dict), phase_iter (iterator)
        """
        self.entities = kwargs.get("entities",[])
        self.status = kwargs.get("status",{})
        self.event = EventManager()        
        return


    def __repr__(self):
        #Short; Otherwise it just explodes as we get recursive representation.
        res = "%s(" % (self.__class__.__name__, )
        #res += "entities=%r, " % self.entities
        #res += "status=%r, " % self.status
        res += ")" 
        return res 

    #TODO: Remove phase property, MAYBE add it dynamically if needed.
    #@property
    #def phase(self):
    #    return self.status["phase"]

    #@phase.setter
    #def phase(self, q):
    #    self.status["phase"] = q
    #    pass

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


