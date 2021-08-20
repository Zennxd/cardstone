import random
import sys
import os
import time

from battleground import Battleground
from api.fetcher import Fetcher
from effect import *
from minion import Minion
from anal.analysis import Analysis

from dill import loads

if __name__ == "__main__":
    iteration_amt: int = 1
    optimization_limit: int = 25

    with Analysis(stdout=(True if iteration_amt < optimization_limit else False)) as anal:
        for iteration in range(iteration_amt):
            Battleground.reset()

            if iteration % 1000 == 0:
                print(iteration)

            # fill both teams
            for _ in range(7):
                with open("minions/hydra.minion", "br") as pickle:
                    m: Minion = loads(pickle.read())
                    m.lineup = Battleground.north_side
                    Battleground.north_side.append(m)

            for _ in range(7):
                with open("minions/super_spore.minion", "br") as pickle:
                    m: Minion = loads(pickle.read())
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
            anal.outcomes.write(f"{iteration}, {outcome}\n")

            print(outcome)
            print("attacks: " + str(Battleground.step - (1 if outcome == "Draw" else 0)))

            # remaining minions
            for side in Battleground.sides():
                for m in side:
                    print(repr(m) + "-" + repr(m.effects))
