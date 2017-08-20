from mafia_engine.base import *
from mafia_engine.entity import *
from mafia_engine.ability import *

from ruamel.yaml import YAML, yaml_object

@yaml_object(Y)
class ConditionChecker(GameObject):
    """Checks if a condition is met, and if so triggers another event."""
    
    #TODO: IMPLEMENT!

    def __init__(self, *args, **kwargs):
        """
        Keys: name, update_on, output_event_type
        """
        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        self.name = kwargs.get("name","")

        self.output_event_type = kwargs.get("output_event_type",None) 
        #NOTE: SHOULD BE OBJECT, NOT TYPE
        
        self.update_on = kwargs.get("update_on",[])

        for e in self.update_on:
            self.subscribe(type(e))

        pass

    def repr_map(self):
        res = super().repr_map()
        res.update( {
            "update_on":self.update_on,
            "output_event_type":self.output_event_type,
            } )

        return res

    def signal(self, event):
        """Override this event to update status, possibly by getting data from the event."""
        pass

    pass

@yaml_object(Y)
class AlignmentEliminationChecker(ConditionChecker):
    """Checks if an Alignment has been eliminated or not."""

    #TODO: IMPLEMENT!

    def __init__(self, *args, **kwargs):
        """
        Keys: name, update_on, output_event_type, alignment
        """
        
        # Before the actions are linked, add on "death"
        if "update_on" in kwargs:
            kwargs["update_on"].append(DeathEvent())
        else:
            kwargs["update_on"] = [DeathEvent()]
            pass

        super().__init__(self, *args, **kwargs)

        self.alignment = kwargs.get("alignment",None)
        self.output_event_type = kwargs.get("output_event_type",AlignmentEliminatedEvent())
        self.eliminated = False
        pass

    def repr_map(self):
        res = super().repr_map()
        res.update( {
            "alignment" : self.alignment,
            "eliminated" : self.eliminated,
            } )
        return res


    def signal(self, event):
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
        outev_type = type(self.output_event_type)
        outev = outev_type(alignment=self.alignment)
        self.send_signal(outev)


    pass
