
from mafia_engine.base import Event, Y
from ruamel.yaml import YAML, yaml_object

#@yaml_object(Y)
class PhaseChangeEvent(Event):
    yaml_tag = u"!PhaseChangeEvent"
    interface = {
        "previous":None,
        "current":None,
        }

#@yaml_object(Y)
class VoteEvent(Event):
    yaml_tag = u"!VoteEvent"
    interface = {
        "actor":None,
        "target":None,
        }

#@yaml_object(Y)
class MKillEvent(Event):
    yaml_tag = u"!MKillEvent"
    interface = {
        "actor":None,
        "target":None,
        }

#@yaml_object(Y)
class LynchEvent(Event):
    yaml_tag = u"!LynchEvent"
    interface = {
        "target":None
        }

#@yaml_object(Y)
class DeathEvent(Event):
    yaml_tag = u"!DeathEvent"
    interface = {
        "target":None
        }

#@yaml_object(Y)
class AlignmentEliminatedEvent(Event):
    yaml_tag = u"!AlignmentEliminatedEvent"
    interface = {
        "alignment":None
        }



