import sys
from mafia_engine.base import GameEngine, GameObject, PhaseGenerator
#from mafia_engine.example.mountainous import *
from mafia_engine.entity import *
from mafia_engine.ability.base import AbilityError
from mafia_engine.ability.simple import *

default_args = []

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
    print("Testing components:")

    #
    ge = GameEngine(
        phases=PhaseGenerator(["day","night"])
        )
    GameObject.default_engine = ge

    #Add mod object
    mod = TestMod(
        name="NowanIlfideme",
        subscriptions=["vote","mkill","phase_change"]
        )

    #Add town team
    tteam = Alignment(name="Town")
    ge.entities.append(tteam)

    #Add mafia team
    mteam = Alignment(name="Mafia")
    ge.entities.append(mteam)

    #Add town players
    for i in range(0,10):
        abils = [
            Vote(name="vote", phase=["day"])
            ]
        trole = Role(
            name = "townie_role",
            alignment=tteam,
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
    for i in range(0,3):
        #TODO: add abilities
        abils = [
            Vote(name="vote", phase=["day"]),
            MKill(name="mkill", phase=["night"])
            ]
        mrole = Role(
            name = "mafioso_role",
            alignment=mteam,
            abilities = abils,
            status = { "alive":True }
            )
        mplayer = Player(
            name = "Mafioso" + str(i),
            roles = [mrole]
            )
        ge.entities.append(mplayer)
    #

    ge

    #Do actions
    #TODO: Make into loop.
    ge.entities[3].roles[0].abilities[0].action(
        actor=ge.entities[3],
        target=ge.entities[4]
        )

    ge.entities[13].roles[0].abilities[0].action(
        actor=ge.entities[13],
        target=ge.entities[7]
        )

    #Should fail
    try:
        ge.entities[13].roles[0].abilities[1].action(
            actor=ge.entities[13],
            target=ge.entities[7]
            )
    except AbilityError as e:
        print(e)
        pass

    ge.next_phase()

    ge.entities[13].roles[0].abilities[1].action(
        actor=ge.entities[13],
        target=ge.entities[7]
        )

    #Should fail
    try:
        ge.entities[12].roles[0].abilities[0].action(
            actor=ge.entities[12],
            target=ge.entities[4]
            )
    except AbilityError as e:
        print(e)
        pass

    ge

    print("Finished.")

    return



if __name__=="__main__":
    args = sys.argv[1:]
    if (len(args)>0): main(args)
    else: main(default_args)
else:
    pass
