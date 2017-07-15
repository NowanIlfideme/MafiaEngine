
class EventManager(object):
    """Manager for in-game events. Works as follows:
    Listeners subscribe to Events.
    Whenever someone wants to raise an event, they Signal it, and all listeners 
        for the event are Signal'd with the event name and params.
    Events get logged in the history.
    """

    def __init__(self):
        self.listeners = {}
        self.logger = None
        return self

    def subscribe(self, event, listener): #I would like to subscribe to "bee facts"
        self.listeners[event].append(listener)
        return

    def unsubscribe(self, event, listener): #please stop sending me bee facts
        self.listeners[event].remove(listener)
        return

    def signal(self, event, parameters, notes=""): #"bee facts" says: "male bees inherit genes only from their mothers"
        #TODO: Add history logging, with notes
        for l in self.listeners[event]:
            try:
                l.signal(event,parameters)
            except:
                #TODO: Handle exception for "function not defined" and such.
                pass
        return

    pass