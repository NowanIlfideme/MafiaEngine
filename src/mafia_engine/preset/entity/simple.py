from ruamel.yaml import YAML, yaml_object
from mafia_engine.base import Y
from mafia_engine.entity import *
from mafia_engine.preset.event.simple import *

@yaml_object(Y)
class MafiaAlignment(Alignment):
    """Denotes the mafia team."""

    yaml_tag = u"!MafiaAlignment"

    def __init__(self, name="", subscriptions=[], status={}, **kwargs):
        """
        Keys: name, subscriptions (list), status (dict)
        """
        if PhaseChangeEvent not in subscriptions:
            subscriptions.append(PhaseChangeEvent)
        super().__init__(name=name, subscriptions=subscriptions, 
                         status=status, **kwargs)
        pass
    
    def signal(self, event):
        super().signal(event)

        if isinstance(event, PhaseChangeEvent):
            self.status["mkill_used"] = False
            pass

        pass

    pass

