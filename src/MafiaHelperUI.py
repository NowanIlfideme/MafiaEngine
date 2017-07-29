import sys, logging
from mafia_engine.base import *
#from mafia_engine.example.mountainous import *
from mafia_engine.entity import *
from mafia_engine.ability.base import *
from mafia_engine.ability.simple import *
from mafia_engine.trigger import *


default_args = []
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) #DEBUG


class TestMod(Moderator):
    """Example moderator."""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        pass

    def signal(self, event, parameters):

        #Get info
        prefix = "-> "

        if "target" in parameters:
            real_target = parameters["target"]
            target = real_target.name
        else: target = "<unknown>"

        if "actor" in parameters:
            actor = parameters["actor"].name
        else: actor = "<unknown>"

        if "alignment" in parameters:
            alignment = parameters["alignment"].name
        else: alignment = "<unknown>"            

        #Get message

        if event=="": pass
        if event=="vote":
            print(prefix + actor + " voted for " + target + "!")
            #TODO: Add voting checks!

        if event=="mkill": print(prefix + actor + " mkilled " + target + "!")

        if event=="phase_change": print(prefix + "Phase changed, now: " + self.engine.phase)

        if event=="death":
            print(prefix + target + " died!")

        if event=="alignment_eliminated":
            print(prefix + alignment + " was eliminated!")
            #TODO: Game-end behavior, for the simple game!
            tmp = self.engine.entity_by_type(Alignment,True)
            tmp.remove(parameters["alignment"])
            print(prefix + tmp[0].name + " has won!")
            self.engine.status["finished"]=True

        pass

def main(args):
    """Console test for the mafia engine."""
    ge = setup(2,1)
    menu(ge)
    return

def setup(n_town, n_mafia):
    """Sets up a mountainous game with the given params"""
    ge = GameEngine(
        phase_gen = PhaseGenerator(["day","night"]),
        status = {
            "phase":None
            }
        )
    GameObject.default_engine = ge

    #Add mod object
    mod = TestMod(
        name="Moderator",
        subscriptions=["vote","mkill",
                       "phase_change",
                       "death",
                       "alignment_eliminated"]
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
            roles = [trole],
            )
        ge.entities.append(tplayer)
        tteam.add(tplayer)
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
            roles = [mrole],
            )
        ge.entities.append(mplayer)
        mteam.add(mplayer)
    #

    #Add condition checkers
    mchecker = AlignmentEliminationChecker(name="mafia_checker", alignment=mteam)
    tchecker = AlignmentEliminationChecker(name="town_checker", alignment=tteam)
    return ge

def menu(ge):
    """Looped menu."""
    options = "help ? list action phase quit exit"
    print(options)

    while True:
        try:
            ln = input("> ")
            if ln.find("list")>=0:
                print("Phase: " + str(ge.phase))
                print([e.name for e in ge.entity_by_type(Actor,True)])
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

            #Check for game end
            if ge.status.get("finished",False):
                break
        except Exception as e:
            print(e)
            pass
    pass

def prompt_action(ge):
    names = [e.name for e in ge.entity_by_type(Actor,True)]
    print(names)
    i_ent = input("Entity (name or index): ")
    try: i_ent = names[int(i_ent)]
    except: pass
    actor = ge.entity_by_name(i_ent)
    
    abil_names = actor.get_ability_names()
    print("Possible actions: " + str(abil_names))
    i_act = input("Action (name or index): ")
    try: i_act = abil_names[int(i_act)]
    except: pass
    
    i_targ = input("Target (name or index): ")
    try: i_targ = names[int(i_targ)]
    except: pass
    target = ge.entity_by_name(i_targ)

    try:
        actor.action(ability=i_act, target=target)
    except AbilityError as e:
        print(e)
    except Exception as e:
        print(e)
        pass
            
    pass

if __name__=="__main__":
    args = sys.argv[1:]
    if (len(args)>0): main(args)
    else: main(default_args)
else:
    pass
