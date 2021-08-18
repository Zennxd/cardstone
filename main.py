import sys
import os
import time

from battleground import Battleground
from minion import Minion
from effect import Poison, Taunt, DivineShield, AOE

if __name__ == "__main__":
    iteration_amt: int = 1

    f = open(f"outcomes/results-{str(int(time.time()))}.csv", "w+")
    f.write("iteration, outcome\n")

    if iteration_amt > 10:
        # printing is most of the work
        sys.stdout = open(os.devnull, 'w')

    for iteration in range(iteration_amt):
        Battleground.reset()

        # fill both teams
        for ii in range(7):  # 1/1 poison divine shield
            m = Minion(attack=1, health=1, lineup=Battleground.north_side)
            m.effects.append(Poison(m))
            m.effects.append(DivineShield(m))
            Battleground.north_side.append(m)

        for ii in range(7):  # stock hydra
            m = Minion(attack=2, health=4, lineup=Battleground.south_side)
            m.effects.append(AOE(m))
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

        print("attacks: " + str(Battleground.step))

        for side in Battleground.sides():
            print("side: ")
            for m in side:
                print(repr(m) + "-" + repr(m.effects))
    f.close()
