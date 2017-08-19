from ruamel.yaml import YAML, yaml_object
from mafia_engine.base import Y
from mafia_engine.entity import *
from mafia_engine.preset.event.simple import *

@yaml_object(Y)
class MafiaAlignment(Alignment):
    """Denotes the mafia team."""

    yaml_tag = u"!MafiaAlignment"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions (list), status (dict)
        """

        if "subscriptions" in kwargs:
            if PhaseChangeEvent not in kwargs["subscriptions"]:
                kwargs["subscriptions"].append(PhaseChangeEvent)
        else: kwargs["subscriptions"] = [PhaseChangeEvent]

        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        pass
    
    def signal(self, event):
        super().signal(event)

        if isinstance(event, PhaseChangeEvent):
            self.status["mkill_used"] = False
            pass

        pass

    pass

