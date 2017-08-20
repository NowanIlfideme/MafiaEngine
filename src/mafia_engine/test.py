import sys
from ruamel.yaml import YAML, yaml_object
from ruamel.yaml.compat import StringIO
from ruamel.yaml.scalarstring import DoubleQuotedScalarString


Y = YAML(typ="safe", pure=True)

# ==============

@yaml_object(Y)
class A(object):
    """Object I want to serialize"""
    yaml_tag = "!Aclass"
    def __init__(self, type):
        self.type = type  #.__class__.__name__

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(
            cls.yaml_tag, u'{}'.format(node.type.__name__)
        )

    @classmethod
    def from_yaml(cls, constructor, node):
        if '.' in node.value:  # in some other module
            m, n = node.value.rsplit('.', 1)
            t = getattr(sys.modules[m], n)
        else:
            t = globals()[node.value]
        cls._check_registered(t,constructor, node)
        return cls(t)
        
    @classmethod
    def _check_registered(cls, t, constructor, node):
        # Check if type "t" is registered in "constr"
        # Note: only a very basic check, 
        # and ideally should be made more secure

        if hasattr(t,"yaml_tag"):
            if t.yaml_tag in constructor.yaml_constructors: 
                
                return
            raise Exception("Error: Tag not registered!")
        else:
            #
            raise Exception("Error: No attribute 'yaml_tag'!")
        pass

    pass

class T1(object):
    """This will be referenced."""
    yaml_tag = u"!T1"
    pass


@yaml_object(Y)
class T2(object):
    """Another referenced object"""
    yaml_tag = u"!T2"

    def __init__(self):
        print("Initializing...")
        pass
    pass

class T2_bad(object):
    """Malicious class impersonating T2"""
    # Note: It's not registered
    yaml_tag = u"!T2"

    def __init__(self):
        print("Evil code here!")
        pass

    pass


class T3(object):
    """Yet another try"""
    yaml_tag = u"!T3"
    pass
Y.register_class(T3)



for t in T1, T2, T2_bad, T3, DoubleQuotedScalarString:
    try:
        print('----------------------')
        x = StringIO()
        s = A(t)
        print('s', s.type)
        Y.dump(s, x)
        print(x.getvalue())
        d = Y.load(x.getvalue())
        print('d', d.type)
        d.type()
    except Exception as e:
        print(e)
        continue
    pass

