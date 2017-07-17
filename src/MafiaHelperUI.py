import sys
from mafia_engine.base import GameEngine, GameObject
#from mafia_engine.example.mountainous import *
from mafia_engine.entity import *
from mafia_engine.ability.simple import *

default_args = []

def main(args):
    print("Testing components:")

    #
    ge = GameEngine()
    GameObject.default_engine = ge

    #Add town team
    tteam = Alignment(name="Town")
    ge.entities.append(tteam)

    #Add mafia team
    mteam = Alignment(name="Mafia")
    ge.entities.append(mteam)

    #Add town players
    for i in range(0,10):
        abils = [
            Vote(name="vote")
            ]
        trole = Role(
            name = "townie_role",
            alignment=tteam,
            abilities = abils
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
            Vote(name="vote"),
            MKill(name="mkill")
            ]
        mrole = Role(
            name = "mafioso_role",
            alignment=mteam,
            abilities = abils
            )
        mplayer = Player(
            name = "Mafioso" + str(i),
            roles = [mrole]
            )
        ge.entities.append(mplayer)
    #

    ge
    print("Finished.")

    return



if __name__=="__main__":
    args = sys.argv[1:]
    if (len(args)>0): main(args)
    else: main(default_args)
else:
    pass
