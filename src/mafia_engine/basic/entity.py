from mafia_engine.base import *
from mafia_engine.entity import Player, Alignment


@yaml_object(Y)
class TownTeam(Alignment):
    """Uninformed majority."""
    yaml_tag = u"!TownTeam"

    def __init__(self, name = '', subscriptions = [], status = {}, members = [], **kwargs):
        
        super().__init__(name, subscriptions, status, members, **kwargs)
        pass

    def signal(self, event):
        
        super().signal(event)
        pass

    pass



@yaml_object(Y)
class MafiaTeam(Alignment):
    """Informed minority."""
    yaml_tag = u"!MafiaTeam"

    def __init__(self, name = '', subscriptions = [], status = {}, members = [], **kwargs):
        
        super().__init__(name, subscriptions, status, members, **kwargs)
        pass

    def signal(self, event):
        
        super().signal(event)
        pass


    pass


@yaml_object(Y)
class ThirdParty(Alignment):
    """Neither town, nor mafia; have own wincons."""
    yaml_tag = u"!ThirdParty"

    def __init__(self, name = '', subscriptions = [], status = {}, members = [], **kwargs):
        
        super().__init__(name, subscriptions, status, members, **kwargs)
        pass

    def signal(self, event):
        
        super().signal(event)
        pass

    pass
