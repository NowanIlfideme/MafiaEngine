import sys, os, logging
import ruamel.yaml
from ruamel.yaml.compat import StringIO
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

def round_trip(ge):
    stream = StringIO()
    Y.dump(ge, stream)
    tmp1 = stream.getvalue()
    
    ge2 = Y.load(tmp1)

    stream2 = StringIO()
    Y.dump(ge2, stream2)
    tmp2 = stream2.getvalue()

    if tmp1==tmp2:
        print("Round-trip test passed.")
    else:
        print("TMP1: \n" + tmp1)
        print("TMP2: \n" + tmp2)
    return tmp1==tmp2

