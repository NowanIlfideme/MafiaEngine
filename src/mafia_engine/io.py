import sys, os, logging, yaml
from mafia_engine.base import *
#from mafia_engine.example.mountainous import *
from mafia_engine.entity import *
from mafia_engine.ability.base import *
from mafia_engine.ability.simple import *
from mafia_engine.trigger import *

def load_game(fname):
    ffname = os.path.realpath(fname)
    res = "<failed>"
    with open(ffname, 'r') as stream:
        try:
            res = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
    return res

def dump_game(ge, fname):
    ffname = os.path.realpath(fname)
    with open(ffname, 'w') as stream:
        yaml.dump(ge, stream)
        print("Dumped to {}".format(ffname))
    return

