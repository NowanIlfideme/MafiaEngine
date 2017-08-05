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
            self.subscribe(e)

        pass

    def __str__(self):
        return "ConditionChecker."+ str(self.name)

    def __repr__(self):
        res = "%s(" % (self.__class__.__name__, )
        res += "name=%r, " % self.name
        res += "update_on=%r, " % self.update_on
        res += "output_event=%r, " % self.output_event
        res += "engine=%r" % self.engine        
        res += ")"
        return res


    def signal(self, event, parameters, notes=""):
        """Override this event to update status, possibly by getting data from the event."""
        pass

    pass

class AlignmentEliminationChecker(ConditionChecker):
    """Checks if an Alignment has been eliminated or not."""

    #TODO: IMPLEMENT!

    def __init__(self, *args, **kwargs):
        """
        Keys: name, update_on, output_event, alignment
        """
        
        # Before the actions are linked, add on "death"
        if "update_on" in kwargs:
            kwargs["update_on"].append("death")
        else:
            kwargs["update_on"] = ["death"]
            pass

        super().__init__(self, *args, **kwargs)

        self.alignment = kwargs.get("alignment",None)
        self.output_event = kwargs.get("output_event","alignment_eliminated") # Overrides super()'s

        self.eliminated = False
        pass

    def __str__(self):
        return "AlignmentEliminationChecker."+ str(self.name)

    def __repr__(self): #TODO!
        res = "%s(" % (self.__class__.__name__, )
        res += "name=%r, " % self.name
        res += "update_on=%r, " % self.update_on
        res += "alignment=%r, " % self.alignment
        res += "output_event=%r, " % self.output_event
        res += "engine=%r" % self.engine        
        res += ")"
        return res


    def signal(self, event, parameters, notes=""):
        """Gets called on death and, possibly, other events.
        Checks whether the alignment has members left."""
        
        if self.eliminated: return

        if len(self.alignment.members)==0:
            pass
        else:
            for member in self.alignment.members:
                if not member.status.get("dead",False):
                    #self.eliminated = False #Don't even have to set it.
                    return
        self.eliminated = True
        self.send_signal(self.output_event, { "alignment":self.alignment } )


    pass
