import sys, os, logging, yaml
from mafia_engine.base import *
from mafia_engine.entity import *
from mafia_engine.ability import *
from mafia_engine.trigger import *
from mafia_engine.io import load_game, dump_game

#imports simple game mechanics
from mafia_engine.preset.simple import *
#from mafia_engine.preset.logic.simple import * 
#from mafia_engine.preset.ability.simple import * 
#from mafia_engine.preset.entity.simple import * 


default_args = [] #[2, 1]
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG) #INFO


def main(*args):
    """Console test for the mafia engine."""

    fname="./resource/save_stage.yaml" #or "../"?

    q = load_game(fname)
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
    menu(ge)

    #dump
    dump_game(ge,fname)
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
        subscriptions=["vote","mkill",
                       "phase_change",
                       "death",
                       "alignment_eliminated"],
        phase_iter = PhaseIterator(phases = ["day","night"]),
        )
    ge.entities.append(mod)

    #Add town team
    tteam = Alignment(name="Town")
    ge.entities.append(tteam)

    #Add mafia team
    mteam = MafiaAlignment(name="Mafia")
    ge.entities.append(mteam)

    
            

    #Add town players
    for i in range(0,n_town):
        abil_vote = Vote(
            name = "vote", 
            restrictions = [
                PhaseRestriction(name="phase_r", phases=["day"]),
                TargetRestriction(name="target_r", target_types=[Actor])
                ]
        )
        abils = [ 
            abil_vote,
            #Vote(name = "vote", phase = ["day"]),
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
        abil_vote = Vote(
            name = "vote", 
            restrictions = [
                PhaseRestriction(name="phase_r", phases=["day"]),
                TargetRestriction(name="target_r", target_types=[Actor])
                ]
            )
        abil_mkill = MKill(
            name = "mkill", 
            restrictions = [
                PhaseRestriction(name="phase_r", phases=["night"]),
                TargetRestriction(name="target_r", target_types=[Actor])
                ]
            )
        abils = [
            abil_vote,
            abil_mkill,
            #Vote(name = "vote", phase = ["day"]),
            #MKill(name = "mkill", phase = ["night"]),
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
                print("Phase: " + str(ge.status["phase"]))
                print([e.name for e in ge.entity_by_type(Actor,True)])
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
            logger.exception()
            pass
    pass

def do_next_phase(ge):
    mod = ge.entity_by_type(Moderator) #Well, actually TestMod
    mod.next_phase()
    pass


def prompt_action(ge):
    names = [e.name for e in ge.entity_by_type(Actor,True)]
    print(names)
    try:
        i_ent = input("Entity (name or index): ")
        try: i_ent = names[int(i_ent)]
        except: pass
        actor = ge.entity_by_name(i_ent)
    
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
            target = ge.entity_by_name(i_targ)

        try:
            actor.action(ability=i_act, target=target)
        except AbilityError as e:
            print("Error with ability: " + str(e))
    except Exception as e:
        print("Error while parsing ability: " + str(e))
    return

if __name__=="__main__":
    args = sys.argv[1:]
    if (len(args)>0): main(*args)
    else: main(*default_args)
else:
    pass
