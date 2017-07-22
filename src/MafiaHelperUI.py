import sys, logging
from mafia_engine.base import GameEngine, GameObject, PhaseGenerator
#from mafia_engine.example.mountainous import *
from mafia_engine.entity import *
from mafia_engine.ability.base import AbilityError
from mafia_engine.ability.simple import *



default_args = []
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class TestMod(Moderator):
    """Example moderator."""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        pass

    def signal(self, event, parameters):
        if event=="":
            pass
        if event=="vote":
            if "actor" in parameters:
                actor = parameters["actor"].name
            else: actor = "<unknown>"
            if "target" in parameters:
                target = parameters["target"].name
            else: target = "<unknown>"
            print(actor + " voted for " + target + "!")
            pass

        if event=="mkill":
            if "actor" in parameters:
                actor = parameters["actor"].name
            else: actor = "<unknown>"
            if "target" in parameters:
                target = parameters["target"].name
            else: target = "<unknown>"
            print(actor + " mkilled " + target + "!")
            pass

        if event=="phase_change":
            print("Phase changed, now: "+self.engine.phase)
            pass


        pass

def main(args):
    #
    ge = setup(5,2)
    menu(ge)
    return

def setup(n_town, n_mafia):
    ge = GameEngine(
        phases=PhaseGenerator(["day","night"])
        )
    GameObject.default_engine = ge

    #Add mod object
    mod = TestMod(
        name="Moderator",
        subscriptions=["vote","mkill","phase_change"]
        )
    ge.entities.append(mod)

    #Add town team
    tteam = Alignment(name="Town")
    ge.entities.append(tteam)

    #Add mafia team
    mteam = Alignment(name="Mafia")
    ge.entities.append(mteam)

    #Add town players
    for i in range(0,n_town):
        abils = [
            Vote(name = "vote", phase = ["day"]),
            ]
        trole = Role(
            name = "townie_role",
            alignment = tteam,
            abilities = abils,
            status = { "alive":True }
            )
        tplayer = Player(
            name = "Townie" + str(i),
            roles = [trole]
            )
        ge.entities.append(tplayer)
    #

    #Add mafia players
    for i in range(0,n_mafia):
        #TODO: add abilities
        abils = [
            Vote(name = "vote", phase = ["day"]),
            MKill(name = "mkill", phase = ["night"]),
            ]
        mrole = Role(
            name = "mafioso_role",
            alignment = mteam,
            abilities = abils,
            status = { "alive":True }
            )
        mplayer = Player(
            name = "Mafioso" + str(i),
            roles = [mrole]
            )
        ge.entities.append(mplayer)
    #
    return ge

def menu(ge):
    """Looped menu."""
    options = "help ? list action phase quit exit"
    print(options)

    while True:
        ln = input("> ")
        if ln.find("list")>=0:
            print([e.name for e in ge.entity_by_type(Actor)])
        if ln.find("action")>=0:
            prompt_action(ge)
        if ln.find("phase")>=0:
            ge.next_phase()
        if ln.find("")>=0:
            pass

        if ln.find("quit")>=0 or ln.find("exit")>=0:
            break
        if ln.find("help")>=0 or ln.find("?")>=0:
            print(options)
    pass

def prompt_action(ge):
    print([e.name for e in ge.entity_by_type(Actor)])
    
    i_ent = input("Entity: ")
    actor = ge.entity_by_name(i_ent)
    
    print("Possible actions: " + str(actor.get_ability_names()))
    i_act = input("Action: ")
    
    
    i_targ = input("Target: ")
    target = ge.entity_by_name(i_targ)

    try:
        actor.action(ability=i_act, target=target)
    except AbilityError as e:
        print(e)
        pass

        
    pass

if __name__=="__main__":
    args = sys.argv[1:]
    if (len(args)>0): main(args)
    else: main(default_args)
else:
    pass
