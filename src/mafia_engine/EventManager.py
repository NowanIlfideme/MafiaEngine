import logging

class EventManager(object):
    """Manager for in-game events. Works as follows:
    Listeners subscribe to Events.
    Whenever someone wants to raise an event, they Signal it, and all listeners 
        for the event are Signal'd with the event name and params.
    Events get logged AND saved in the history.
    History allows one to resume a game from a particular state.
    """

    def __init__(self):
        self.listeners = {}
        self.logger = logging.getLogger(__name__)  #normal Python logger
        self.history = None #TODO: Add history, to allow pausing and resuming of games.
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