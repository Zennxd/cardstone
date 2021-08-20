import sys
import os
import time
from random import randint

from dill import loads

from battleground import Battleground
from effect import *
from minion import Minion

if __name__ == "__main__":
    iteration_amt: int = 1

    file_name: str = f"results-{str(int(time.time()))}"

    f = open(f"outcomes/{file_name}.csv", "w+")
    f.write("iteration, outcome\n")

    if iteration_amt > 25:
        # printing is most of the work
        sys.stdout = open(os.devnull, 'w')

    for iteration in range(iteration_amt):
        Battleground.reset()

        if iteration % 1000 == 0:
            print(iteration)

        # fill both teams
        for _ in range(6):
            with open("minions/hydra.minion", "br") as file:
                m: Minion = loads(file.read())
                m.lineup = Battleground.north_side

                Battleground.north_side.append(m)
        for _ in range(6):
            with open("minions/super_spore.minion", "br") as file:
                m: Minion = loads(file.read())
                m.lineup = Battleground.south_side
                Battleground.south_side.append(m)

        # ----------- #

        Battleground.fight()  # (this calls what is essentially the main loop of the application)

        # ----------- #

        outcome: str = "Draw"
        if not Battleground.north_side.defeated() and Battleground.south_side.defeated():
            outcome = "North won"
        elif Battleground.north_side.defeated() and not Battleground.south_side.defeated():
            outcome = "South won"
        f.write(f"{iteration}, {outcome}\n")

        print(outcome)
        print("attacks: " + str(Battleground.step - (1 if outcome == "Draw" else 0)))

        # remaining minions
        for side in Battleground.sides():
            for m in side:
                print(repr(m) + "-" + repr(m.effects))
