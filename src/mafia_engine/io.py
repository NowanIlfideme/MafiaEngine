import sys, os, logging
import ruamel.yaml
from mafia_engine.base import Y
#from mafia_engine.entity import *
#from mafia_engine.ability import *
#from mafia_engine.trigger import *

def load_game(fname):
    ffname = os.path.realpath(fname)
    res = "<failed>"
    with open(ffname, 'r') as stream:
        try:
            res = Y.load(stream)
        except ruamel.yaml.YAMLError as exc:
            print(exc)
            return None
    return res

def dump_game(ge, fname):
    ffname = os.path.realpath(fname)
    try:
        with open(ffname, 'w') as stream:
            Y.dump(ge, stream)
            print("Dumped to {}".format(ffname))
    except Exception as e:
        raise e
    return

