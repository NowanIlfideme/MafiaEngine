import sys
from ruamel.yaml import YAML, yaml_object

Y = YAML(typ="safe",pure=True)

# ==============

@yaml_object(Y)
class A(object):
    """Object I want to serialize"""
    yaml_tag = "!Aclass"
    def __init__(self, type):
        self.type = type
    pass

class T1(object):
    """This will be referenced."""
    pass

@yaml_object(Y)
class T2(object):
    """Another referenced object"""
    pass

class T3(object):
    """Yet another try"""
    pass
Y.register_class(T3.__class__)

# ==============

Y.dump(A(T1), sys.stdout)
Y.dump(A(T2), sys.stdout)
Y.dump(A(T3), sys.stdout)
Y.dump(A(int), sys.stdout)

Y.dump(A(str), sys.stdout)
Y.dump(A(str), sys.stdout)
Y.dump(A(str), sys.stdout)


Y.dump(A(T1), sys.stdout)
Y.dump(A(T1), sys.stdout)

