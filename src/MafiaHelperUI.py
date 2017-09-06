
import sys, os, sys, logging, yaml

"""
os.chdir("C:\\Users\\anato\\MafiaEngine\\src\\")
"""

from mafia_engine.base import *
from mafia_engine.entity import *
from mafia_engine.ability import *
from mafia_engine.trigger import *
from mafia_engine.io import load_game, dump_game, round_trip

#imports simple game mechanics
from mafia_engine.preset.simple import *
#from mafia_engine.preset.logic.simple import * 
#from mafia_engine.preset.ability.simple import * 
#from mafia_engine.preset.entity.simple import * 


default_args = [] #[2, 1]
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) #INFO # DEBUG


def bmain(*args):
    ge = setup2(2, 1)

    pass


def setup2(n_town, n_mafia):
    """Sets up a mountainous game with the given params"""
    ge = GameEngine(
        status = {
            "phase":None
            }
        )
    GameObject.default_engine = ge

    #Add town team
    tteam = Alignment(name="Town")
    ge.entity.members.append(tteam)
    tchecker = AlignmentEliminationChecker(name="town_checker", alignment=tteam)

    round_trip(ge)

    #Add mod object
    mod = TestMod(
        name="Moderator",
        subscriptions=[
            VoteEvent,
            MKillEvent,
            PhaseChangeEvent,
            DeathEvent,
            AlignmentEliminatedEvent,
        ],
        phase_iter = PhaseIterator(phases = ["day","night"]),
        )
    ge.entity.members.append(mod)

    #round_trip(mod)


    round_trip(ge)

    round_trip(ge)

    #Add mafia team
    mteam = MafiaAlignment(name="Mafia")
    ge.entity.members.append(mteam)

    round_trip(ge)
            

    #Add town players
    for i in range(0,n_town):
        tplayer = Player(
            name = "Townie" + str(i),
            members = [
                VoteAbility(name = "vote"),
                ],
            #status = { "alive":True },
            )
        tteam.members.append(tplayer)
    #

    round_trip(ge)

    #Add mafia players
    for i in range(0,n_mafia):
        mplayer = Player(
            name = "Mafioso" + str(i),
            members = [
                VoteAbility(name = "vote"),
                MKillAbility(name = "mkill", alignment=mteam),
                ],
            #status = { "alive":True },
            )
        mteam.members.append(mplayer)
    #

    round_trip(ge)
    
    
    #Add condition checkers
    mchecker = AlignmentEliminationChecker(name="mafia_checker", alignment=mteam)
    

    round_trip(ge)

    return ge

def main(*args):
    """Console test for the mafia engine."""

    raw_fname="../resource/save_stage.yaml" #or "../"?
    fname = os.path.join(os.path.dirname(__file__), raw_fname)
    q = load_game(fname)

    #temp - roundtrip


    need_new_game = q is None or q.status.get("finished",False) is True
    if need_new_game:
        print("Previous game already finished or couldn't load.")
        if len(args)==0:
            n_town = int(input("Number of town: "))
            n_mafia = int(input("Number of mafia: "))
        else:
            n_town = args[0]
            n_mafia = args[1]
        ge = setup(n_town, n_mafia)
    else:
        print("Continuing from previous game.")
        ge = q
    #round_trip(ge)
    menu(ge)

    #dump
    dump_game(ge,fname)

    #Y.dump(ge.entity.members_by_type(TestMod, True)[0], sys.stdout)
    return

def setup(n_town, n_mafia):
    """Sets up a mountainous game with the given params"""
    ge = GameEngine(
        status = {
            "phase":None
            }
        )
    GameObject.default_engine = ge

    #Add mod object
    mod = TestMod(
        name="Moderator",
        subscriptions=[
            VoteEvent,
            MKillEvent,
            PhaseChangeEvent,
            DeathEvent,
            AlignmentEliminatedEvent,
        ],
        phase_iter = PhaseIterator(phases = ["day","night"]),
        )
    ge.entity.members.append(mod)

    #Add town team
    tteam = Alignment(name="Town")
    ge.entity.members.append(tteam)

    #Add mafia team
    mteam = MafiaAlignment(name="Mafia")
    ge.entity.members.append(mteam)

    
            

    #Add town players
    for i in range(0,n_town):
        tplayer = Player(
            name = "Townie" + str(i),
            members = [
                VoteAbility(name = "vote"),
                ],
            #status = { "alive":True },
            )
        tteam.members.append(tplayer)
    #

    #Add mafia players
    for i in range(0,n_mafia):
        mplayer = Player(
            name = "Mafioso" + str(i),
            members = [
                VoteAbility(name = "vote"),
                MKillAbility(name = "mkill", alignment=mteam),
                ],
            #status = { "alive":True },
            )
        mteam.members.append(mplayer)
    #

    #Add condition checkers
    mchecker = AlignmentEliminationChecker(name="mafia_checker", alignment=mteam)
    tchecker = AlignmentEliminationChecker(name="town_checker", alignment=tteam)
    return ge

def get_alive_actors(ge):
    lamb = lambda x: isinstance(x, Actor) and not x.status.get("dead",False)
    return ge.entity.members_by_lambda(lamb,True)

def menu(ge):
    """Looped menu."""
    options = "help ? list action phase quit exit"
    print(options)

    while True:
        try:
            ln = input("> ")
            if ln.find("list")>=0:
                print("Phase: " + str(ge.status["phase"]))
                print([e.name for e in get_alive_actors(ge)])
            if ln.find("action")>=0:
                prompt_action(ge)
            if ln.find("phase")>=0:
                do_next_phase(ge)
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
            logger.exception(e)
            pass
    pass

def do_next_phase(ge):
    mod = ge.entity.members_by_type(Moderator, True)[0] #Well, actually TestMod
    mod.next_phase()
    pass


def prompt_action(ge):
    names = [e.name for e in get_alive_actors(ge)]
    print(names)
    try:
        i_ent = input("Entity (name or index): ")
        try: i_ent = names[int(i_ent)]
        except: pass
        actor = ge.entity.members_by_name(i_ent, True)[0]
    
        abil_names = actor.get_ability_names()
        if len(abil_names)==1:
            i_act = abil_names[0]
            print("Action: " + str(i_act) + " (only possible one).")
        else:
            print("Possible actions: " + str(abil_names))
            i_act = input("Action (name or index): ")
            try: i_act = abil_names[int(i_act)]
            except: pass
            pass
    
        i_targ = input("Target (name or index): ")
        try: i_targ = names[int(i_targ)]
        except: pass
        
        if i_targ=="None": 
            target = None
        else: 
            target = ge.entity.members_by_name(i_targ,True)[0]

        try:
            actor.action(ability=i_act, target=target)
        except AbilityError as e:
            print("Error with ability: " + str(e))
    except Exception as e:
        print("Error while parsing ability: " + str(e))
        raise
    return

if __name__=="__main__":
    args = sys.argv[1:]
    if (len(args)>0): main(*args)
    else: main(*default_args)
else:
    pass
