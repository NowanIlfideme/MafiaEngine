from mafia_engine.entity import *

class MafiaAlignment(Alignment):
    """Denotes the mafia team."""

    yaml_tag = u"!MafiaAlignment"

    def __init__(self, *args, **kwargs):
        """
        Keys: name, subscriptions (list), status (dict)
        """

        if "subscriptions" in kwargs:
            if "phase_change" not in kwargs["subscriptions"]:
                kwargs["subscriptions"].append("phase_change")
        else: kwargs["subscriptions"] = ["phase_change"]

        super().__init__(self, *args, **kwargs)
        #TODO: Implement
        pass
    
    def signal(self, event, parameters, notes=""):
        super().signal(event, parameters, notes)

        if event=="phase_change":
            self.status["mkill_used"] = False
            pass

        pass

    pass

