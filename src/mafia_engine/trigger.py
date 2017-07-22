from mafia_engine.base import *
from mafia_engine.entity import *
from mafia_engine.ability.base import *

class ConditionChecker(GameObject):
    """Checks if a condition is met, and if so triggers another event."""
    
    #TODO: IMPLEMENT!

    def __init__(self, *args, **kwargs):
        """
        Keys: name, update_on, output_event
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        self.name = kwargs.get("name","")
        self.output_event = kwargs.get("output_event",None)
        
        self.update_on = kwargs.get("update_on",[])

        for e in self.update_on:
            self.engine.event_manager.subscribe(e,self)

        pass

    def __repr__(self):
        return "ConditionChecker."+ str(self.name)

    def signal(self, event, parameters, notes=""):
        """Override this event to update status, possibly by getting data from the event."""
        pass

    pass

