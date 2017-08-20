import logging
import sys

from ruamel.yaml import YAML, yaml_object

Y = YAML(typ='safe', pure=True)
#Y.default_flow_style=False

@yaml_object(Y)
class RepresentableObject(object):

    def __init__(self):
        pass

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        #res = super().repr_map()
        #res.update( {} )
        res = {}
        return res

    def __str__(self): 
        if hasattr(self,"name"):
            return "%s.%s" % (self.__class__.__name__, self.name)
        else: return "<%s>" % (self.__class__.__name__)

    def __repr__(self):
        res = "%s(" % self.__class__.__name__
        res += ", ".join(str(k)+"="+repr(v) for k,v in self.repr_map().items())
        res += ")" 
        return res
    
    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_mapping(cls.yaml_tag,
            node.repr_map())
    
    @classmethod
    def from_repr(cls, txt):

        txt = node.value
        cls_name, raw_args = txt.split('(',1)
        raw_args = raw_args.rsplit(')',1)[0]
        args = raw_args.split(", ")
        kwargs = {}
        for arg in args:
            k, v = args.split('=',1)
            kwargs[k]=v
            #TODO: Fix! "v" is a string now, should be object
        res = cls(**kwargs)
        return res

    @classmethod
    def bad_from_yaml(cls, constructor, node):
        #TODO: read representation!
        
        #instance = cls()
        #yield instance

        argmap = {}
        for nv in node.value:
            attr = nv[0].value
            obj = constructor.construct_object(nv[1], deep=False)
            argmap[attr] = obj
            pass
        
        instance = cls(**argmap)
        return instance

    pass



@yaml_object(Y)
class GameObject(RepresentableObject):
    """Defines a game object. This helps in finding the object's environment 
    (i.e. the current game, symbolized by a GameEngine reference).
    Through that, it can find the EventManager, other GameObjects, etc."""

    yaml_tag = u"!GameObject"
    #hidden_fields = []
    default_engine = None

    def __init__(self, *args, **kwargs):
        """
        Keys: engine, name, subscriptions
        """
        self.engine = kwargs.get("engine", self.default_engine)
        self.name = kwargs.get("name","")

        to_subscribe = kwargs.get("subscriptions",[])
        for event in to_subscribe:
            self.subscribe(event)
            pass

        return

    @property
    def subscriptions(self):
        return self.engine.event.get_subscriptions_of(self)

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            'name':self.name,
            #'subscriptions':self.subscriptions,
            'engine':self.engine,
           } )
        return res


    def signal(self, event):
        """Signals $self that $event happened.
        Override this."""
        pass

    def send_signal(self, event):
        """Signal the event manager that $event happened."""
        self.engine.event.signal(event)

    def subscribe(self, event):
        """Subscribe $self (as listener) to $event."""
        try:
            self.engine.event.subscribe(event,self)
        except: 
            print("OOPS")
            #raise
        pass

    def unsubscribe(self, event):
        """Unsubscribe $self (as listener) from $event."""
        self.engine.event.unsubscribe(event,self)
        pass

    pass

@yaml_object(Y)
class ProxyObject(GameObject): 
    """Base class for temporary/use objects."""
    # TODO: Implement!
    pass


@yaml_object(Y)
class HistoryManager(RepresentableObject):
    """Saves all events in chronological and searchable order.
    TODO: Implement!
    """

    yaml_tag = u"!HistoryManager"

    def __init__(self, *args, **kwargs):
        """Keys: <none>"""
        pass

    def __str__(self): return "HistoryManager"

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { } )
        return res

    def signal(self, event):
        """Saves an event to history. TODO: Implement."""
        pass

    pass


@yaml_object(Y)
class Entity(GameObject):
    """Denotes a game-world entity. Base class."""

    yaml_tag = u"!Entity"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions (list), status (dict), members (list)
        """

        super().__init__(self, *args, **kwargs)

        #Note: subscriptions handled in GameObject
        self.status = kwargs.get("status",{})
        self.members = kwargs.get("members",[])
        pass

    def signal(self, event):
        """Gets called when subscribed to other events."""
        pass # Override.

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            'status':self.status,
            'members':self.members,
            } )
        return res

    # Work with members:

    def members_by_lambda(self, lamb, recursive = False):
        """Gets members for whom $lamb(e) is True"""
        found_membs = []
        if recursive:
            for e in self.members:
                if lamb(e): found_membs.append(e)
                try:
                    tmp = e.members_by_lambda(lamb, recursive)
                    found_membs.extend(tmp)
                except: pass #we can't tell whether they implement
        else:
            for e in self.members:
                if lamb(e): found_membs.append(e)
        return found_membs

    def members_by_name(self, name, recursive = False):
        """Gets entities whose name is $name."""
        return self.members_by_lambda(
            lambda e: e.name==name, recursive)

    def members_by_type(self, type, recursive = False):
        """Gets members who are instances of $type."""
        return self.members_by_lambda(
            lambda e: isinstance(e, type), recursive)

    def members_by_status(self, status, recursive = False):
        """Gets members whose $status exists and conforms to it."""
        lamb = lambda x : hasattr(x,"status") and all(
            [k in x.status and x.status[k]==status[k] for k in status] )
        return self.members_by_lambda(lamb, recursive)
    
    pass

@yaml_object(Y)
class EntityManager(Entity):
    """Global entity manager."""

    yaml_tag = u"!EntityManager"

    # TODO: Implement!

    pass





#@yaml_object(Y)
class Event(object):
    """In-game event. 'interface' represents arguments 
    that will be added to definition, along with their
    default values. Base class."""

    yaml_tag = u"!Event"
    interface = {} # name:"<empty event>" }

    def __init__(self, *args, **kwargs):
        super().__init__()
        for att in self.interface:
            setattr(self, att, kwargs.get(att,self.interface[att]))
        # Extend or override for own behavior
        pass

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            'interface':self.interface,
            } )
        return res

    pass


@yaml_object(Y)
class Action(GameObject):
    """In-game action, with automatic event handling.
    Actions are working types. Base class."""

    def action(self, *args, **kwargs):
        """Active portion of the class. Override this!"""
        self.engine.event.signal(
            Event(name="Dummy action with args: %s" % kwargs)
            )
        pass

    def __call__(self, *args, **kwargs):
        """Performs the Action. 
        Given as convenience - do not override!"""
        self.action(*args, **kwargs)
        pass

    def repr_map(self):
        return super().repr_map()

    pass



@yaml_object(Y)
class EventManager(RepresentableObject):
    """Manager for in-game events. Works as follows:
    Listeners subscribe to Events.
    Whenever someone wants to raise an event, they Signal it, and all listeners 
        for the event are Signal'd with the event name and params.
    Events get logged AND saved in the history.
    History allows one to resume a game from a particular state.
    """

    yaml_tag = u"!EventManager"

    def __init__(self, *args, **kwargs):
        """
        Keys: listeners (dict), history (HistoryManager)
        """
        self.listeners = kwargs.get("listeners",{}) # event_obj : set(obj)
        self.history = kwargs.get("history",HistoryManager())
        return

    @property
    def logger(self): #lazily add when needed, also helps not f*** up serialization
        if not hasattr(self, "_logger"):
            setattr(self, "_logger", logging.getLogger(__name__))  #normal Python logger
        return self._logger

    @property
    def _listeners(self):
        # returns all types
        res = {}
        for k in self.listeners:
            res[type(k)]=k
        return res

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            'listeners':self.listeners,
            'history':self.history,
            } )
        return res

    def get_subscriptions_of(self, obj):
        # Returns the subscriptions of an object, as Types
        res = [type(k) for k,v in self.listeners.items() if vars==obj]
        return res

    def subscribe(self, event_type, listener): 
        """Subscribe @listener to @event (i.e. to a Type). 
        It will be signal()'d with information when it happens."""

        if event_type not in self._listeners:
            self.listeners[event_type()] = [] #or set()?
        e = self._listeners[event_type]

        self.listeners[e].append(listener) #if set(), then add

        self.logger.debug(
            "Subscription to: "+str(event_type.__name__)
            +" by "+str(listener)
            )
        return

    def unsubscribe(self, event_type, listener): 
        """No longer get signal()'d with regards to @event."""
        if event_type in self._listeners:
            e = self._listeners[event_type]
            self.listeners[e].remove(listener)
            
            if len(self.listeners[e])==0:
                del(self.listeners[e])
            self.logger.debug(
                "Unsubscription from: "+str(event_type.__name__)
                +" by "+str(listener)
                )
        return

    def signal(self, event): 
        """Notify all subscribers of @event by calling signal(@event),
        where the Type of the @event determines who will recieve it."""

        self.history.signal(event)
        event_type = type(event)

        if event_type in self._listeners:
            e = self._listeners[event_type]
            self.logger.debug("Signaling " + str(len(self.listeners[e])) 
                              + " with " + str(event))
            for l in self.listeners[e]:
                try:
                    l.signal(event)
                except:
                    self.logger.exception("Could not signal.")
                    raise
        else:
            self.logger.debug("Event "+str(event)+" happened, but 0 listeners.")
        return

    pass





@yaml_object(Y)
class GameEngine(RepresentableObject):
    """Defines a complete Mafia-like game."""

    yaml_tag = u"!GameEngine"

    def __init__(self, *args, **kwargs):
        """
        Keys: entity (EntityManager), status (dict), event (EventManager)
        """
        self.status = kwargs.get("status",{})
        self.event = kwargs.get("event",EventManager())
        self.entity = kwargs.get("entity",
                                 EntityManager(
                                     engine=self,
                                     name="all_entities"
                                     )
                                 )
        return

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            'entity':self.entity,
            'status':self.status,
            'event':self.event,
            } )
        return res

    def __repr__(self):
        #Short; Otherwise it just explodes as we get recursive representation.
        #Even status might be recursive!

        res = "%s(" % self.__class__.__name__
        #res += "entity=%r, " % self.entity
        #res += "status=%r, " % self.status
        res += ")" 
        return res 

    pass


