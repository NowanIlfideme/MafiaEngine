import logging
import warnings
import sys
import inspect

from copy import copy as shallowcopy, deepcopy

from ruamel.yaml import YAML, yaml_object

##############################
###   DEFAULTS
##############################

Y = YAML(typ='safe', pure=True)
#Y.default_flow_style=False

__default_priorty__ = -1

##############################
###   BASE  CLASSES
##############################

class MafiaException(Exception): """Base class for MafiaEngine errors."""
class EntityError(MafiaException): """Error with regards to entities."""
class EventError(MafiaException): """Error with regards to events."""
class AbilityError(MafiaException): """Something wrong with an ability."""


@yaml_object(Y)
class RepresentableObject(object):

    def __init__(self, **kwargs):
        # Shouldn't have any kwargs
        if len(kwargs)>0: 
            warnings.warn(
                "YamlableObject got unused kwargs: %s" 
                % str(kwargs), stacklevel=2)
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
    def from_repr(cls, txt):
        # NOTE: Doesn't work. Sorry.
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


    pass

@yaml_object(Y)
class YamlableObject(RepresentableObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_mapping(cls.yaml_tag,
            node.repr_map())
    
    pass


@yaml_object(Y)
class GameObject(YamlableObject):
    """Defines a game object. This helps in finding the object's environment 
    (i.e. the current game, symbolized by a GameEngine reference).
    Through that, it can find the EventManager, other GameObjects, etc."""

    yaml_tag = u"!GameObject"
    default_engine = None

    def __init__(self, engine=None, name="", subscriptions=[], **kwargs):
        """
        Keys: engine, name, subscriptions
        """
        super().__init__(**kwargs)
        self.engine = self.default_engine if (engine is None) else engine
        self.name = name

        # subscriptions are immediately handled by the event handler,
        # so we don't save them in this object.
        for event in subscriptions: 
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
            'engine':self.engine,
           } )
        return res


    def signal(self, event):
        """Event manager signals $self that $event happened.
        Override this."""
        pass

    def send_signal(self, event):
        """Signal the event manager that $event happened."""
        self.engine.event.signal(event)

    def subscribe(self, event, priority=__default_priorty__):
        """Subscribe $self (as listener) to $event."""
        self.engine.event.subscribe(event, self, priority)
        pass

    def unsubscribe(self, event):
        """Unsubscribe $self (as listener) from $event."""
        self.engine.event.unsubscribe(event,self)
        pass

    pass

@yaml_object(Y)
class ProxyObject(GameObject): 
    """Base class for temporary-use objects."""

    yaml_tag=u"ProxyObject"
    # TODO: Implement! When they become required.
    pass


##############################
###   EVENT and ACTION
##############################


@yaml_object(Y)
class Event(RepresentableObject):
    """In-game event. 'interface' represents arguments 
    that will be added to definition, along with their
    default values. Base class."""

    yaml_tag = u"!Event"
    interface = {} # name:"<empty event>" }

    def __init__(self, **kwargs):
        super().__init__()
        for att in self.interface:
            setattr(self, att, kwargs.get(att,self.interface[att]))
        not_used = {q:v for q,v in kwargs.items() if q not in self.interface}
        if len(not_used)>0:
            warnings.warn("Arguments not in interface: %s" % (not_used,))
        # Extend or override for own behavior
        pass

    def same_type(a, b):
        """Determines if $b is same type as $a (or $self)."""
        return ( type(a)==type(b) )

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            #'interface':self.interface,
            } )
        return res

    pass

@yaml_object(Y)
class Action(GameObject):
    """In-game action, with automatic event handling.
    Actions are working types. Base class."""

    def _action(self, **kwargs):
        """Active portion of the class. Override this!"""
        print("Please override %s._action()!" % self.__class__.__name__)
        pass

    def __call__(self, **kwargs):
        """Performs the Action and calls necessary events."""

        pre_act = PreActionEvent(action=self)
        self.engine.event.signal(pre_act)

        self._action(**kwargs)

        post_act = PostActionEvent(action=self)
        self.engine.event.signal(post_act)
        pass

    def repr_map(self):
        return super().repr_map()

    def same_type(a, b):
        """Returns whether $a (self) and %b are of the same type 
        (not necessarily by class)."""
        return ( type(a)==type(b) )

    pass


@yaml_object(Y)
class ActionEvent(Event):
    """Event, caused by Action, with a link to said Action. """

    yaml_tag = u"!ActionEvent"
    interface = {'action':Action()}

    def __init__(self, action=Action(), **kwargs):
        super().__init__(action=action, **kwargs) #sets attributes
        pass

    def same_type(a, b):
        return super().same_type(b) and a.action.same_type(b)
    pass

@yaml_object(Y)
class PreActionEvent(ActionEvent):
    """ActionEvent that signifies the Action is about to occur. """
    yaml_tag = u"!PreActionEvent"
    pass

@yaml_object(Y)
class PostActionEvent(ActionEvent):
    """ActionEvent that signifies that Action has already occured."""
    yaml_tag = u"!PostActionEvent"
    pass

@yaml_object(Y)
class TriggeredEvent(Event):
    """Base Event for signifying the fact that an object was triggered."""
    yaml_tag = u"!TriggeredEvent"
    pass

@yaml_object(Y)
class EngineEvent(Event):
    """Base Event for signifying that something happend with the Engine."""
    yaml_tag = u"!EngineEvent"
    pass




##############################
###   ENTITY
##############################

@yaml_object(Y)
class Entity(GameObject):
    """Denotes a game-world entity. Base class."""

    yaml_tag = u"!Entity"

    def __init__(self, name="", subscriptions=[], status={}, members=[], 
                 engine=None, **kwargs):
        super().__init__(name=name, subscriptions=subscriptions, 
                         engine=engine, **kwargs)
        self.status = status.copy()
        self.members = members.copy()
        pass

    def signal(self, event):
        """Gets called when subscribed to other events. Override this!"""
        pass

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            'status':self.status,
            'members':self.members,
            } )
        return res


    # Helper functions for working with members:

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



##############################
###   GAME ENGINE
##############################

@yaml_object(Y)
class HistoryManager(YamlableObject):
    """Saves all events in chronological and searchable order.
    TODO: Implement!
    """

    yaml_tag = u"!HistoryManager"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

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
class SingleSubscription(YamlableObject):
    """Manages subscribers of a single Event."""

    yaml_tag = u"!SingleSubscription"

    #self.event - event object
    #self.subscribers - [ (priority, object) ]

    def __init__(self, event, subscribers = []):
        if inspect.isclass(event):
            self.event = event()
        else: self.event = shallowcopy(event)
        self.subscribers = subscribers

        pass

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            'event':self.event,
            'subscribers':self.subscribers,
            } )
        return res

    def ordered_subscribers(self):
        """Returns subscribers, in order of descending priority."""
        tmp = sorted(self.subscribers, key=lambda x: x[0], reverse=True)        
        return [t[1] for t in tmp]

    def add_subscriber(self, obj, priority = __default_priorty__):
        """Subscribes obj to self."""
        self.subscribers.append( (priority, obj) )
        pass

    def remove_subscriber(self, obj):
        """Removes obj from self.subscribers."""
        i=0
        while i<len(self.subscribers):
            p, o = self.subscribers[i]
            if o is obj: del self.subscribers[i]
            else: i+=1
        pass

    def has_subscriber(self, obj):
        """Checks whether obj is a subscriber."""
        for p, o in self.subscribers:
            if o is obj: return True
        return False



    def is_my_event(self, event):
        """Checks whether 'event' is of correct type 
        (not necessarily same class)."""
        return self.event.same_type(event)

    pass

@yaml_object(Y)
class EventManager(YamlableObject):
    """Manager for in-game events. Works as follows:
    Listeners subscribe to Events.
    Whenever someone wants to raise an event, they Signal it, and all listeners 
        for the event are Signal'd with the event name and params.
    Events get logged AND saved in the history.
    History allows one to resume a game from a particular state.
    """

    _implementation_details = """
    self._listeners is a map of: event_object : set(listener_obj)
    self.listeners is a property, where
        getter returns map of: event_type : set(listener_obj)
        setter is non-existent
    """

    yaml_tag = u"!EventManager"

    def __init__(self, events=[], history=None):
        self.events = events # list of SingleSubscription
        self.history = HistoryManager() if (history is None) else history
        return

    @property
    def logger(self): #lazily add when needed, also helps not f*** up serialization
        if not hasattr(self, "_logger"):
            setattr(self, "_logger", logging.getLogger(__name__))
        return self._logger

    def repr_map(self):
        """Map to use as representation (to create your self).
        Override or extend this for each child!"""

        res = super().repr_map()
        res.update( { 
            'events':self.events,
            'history':self.history,
            } )
        return res

    def get_subscriptions_of(self, obj):
        # Returns the subscriptions of an object, as objects
        
        res = []
        for ss in self.events:
            if ss.has_subscriber(obj):
                res.append(ss.event)
            pass
        return res

    def subscribe(self, event, listener, priority=-1): 
        """Subscribe @listener to @event (or, if it's an object, to its Type). 
        It will be signal()'d with information when it happens."""

        if inspect.isclass(event): event = event() # event is now an Object
        if not isinstance(event, Event):
            raise EventError("Attempted to subscribe to a non-Event.")

        # TODO: Implement!
        found = False
        for ss in self.events:
            if ss.is_my_event(event):
                found = True
                ss.add_subscriber(listener, priority)
                break
        if not found:
            self.events.append( SingleSubscription(
                event, subscribers=[(priority, listener)] ) )
            pass

        # if str(listener)=="Actor.": print("WAT")
        self.logger.debug("Subscription to %s by %s " % (event, listener) )
        return

    def unsubscribe(self, event, listener): 
        """No longer get signal()'d with regards to @event."""

        found = False
        for ss in self.events:
            if ss.is_my_event(event):
                found = True
                ss.remove_subscriber(listener)
                break
            pass

        if found:
            self.logger.debug("Unsubscription from %s by %s "  % (event, listener) )
        else:
            self.logger.debug("Can't unsub from %s, %s is not a listener." % (event, listener) )
            pass
        
        return

    def signal(self, event): 
        """Notify all subscribers of @event by calling signal(@event),
        where the Type of the @event determines who will recieve it."""

        self.history.signal(event)

        found = False
        listeners = []
        for ss in self.events:
            if ss.is_my_event(event):
                found = True
                listeners = ss.ordered_subscribers()
                break
        
        if len(listeners)==0:
            self.logger.debug("Event happened, but 0 listeners: %s" % (event) )
        else:
            self.logger.debug("Signaling %s with %s" % 
                                (len(listeners), event) )
            for l in listeners:
                try: l.signal(event)
                except:
                    self.logger.exception("Could not signal %l with event %s." % 
                                          (l, event) )
                    raise
        return

    pass





@yaml_object(Y)
class GameEngine(YamlableObject):
    """Defines a complete Mafia-like game."""

    yaml_tag = u"!GameEngine"

    def __init__(self, status={}, event=None, entity=None, **kwargs):
        """
        Keys: entity (EntityManager), status (dict), event (EventManager)
        """
        super().__init__(**kwargs)
        self.status = status
        self.event = EventManager() if (event is None) else event
        if entity is None:
            self.entity = EntityManager(
                engine=self, name="all_entities" )
        else: self.entity = entity
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
        return "%s(...)" % self.__class__.__name__

    pass


