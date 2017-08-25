from mafia_engine.base import *
from mafia_engine.entity import *
from mafia_engine.ability import *

from ruamel.yaml import YAML, yaml_object

@yaml_object(Y)
class ConditionChecker(GameObject):
    """Checks if a condition is met, and if so triggers another event."""
    
    def __init__(self, name="", output_event_type=None, 
                 subscriptions=[], **kwargs):
        """
        Keys: name, update_on, output_event_type
        """
        super().__init__(name=name, subscriptions=subscriptions, **kwargs)

        self.output_event_type = output_event_type
        #NOTE: SHOULD BE OBJECT, NOT TYPE
        
        pass

    def repr_map(self):
        res = super().repr_map()
        res.update( {
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

    def __init__(self, name="", alignment=None, eliminated = False, **kwargs):
        super().__init__(name=name, subscriptions = [DeathEvent],
                         output_event_type=AlignmentEliminatedEvent(), **kwargs)
        self.alignment = alignment
        self.eliminated = eliminated
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
            pass #eliminated
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
