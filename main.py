import random
import sys
import os
import time

from battleground import Battleground
from api.fetcher import Fetcher
from effect import *
from minion import Minion
from anal.analysis import Analysis

if __name__ == "__main__":
    iteration_amt: int = 100

    if iteration_amt > 25:
        # printing is most of the work
        sys.stdout = open(os.devnull, 'w')

    with Analysis() as anal:
        for iteration in range(iteration_amt):
            Battleground.reset()

            if iteration % 1000 == 0:
                print(iteration)

            # fill both teams
            cards = Fetcher.fetch()
            for side in Battleground.sides():
                for l in range(6):
                    rnd = random.choice(cards)
                    anal.lineups.write(rnd["name"] + (", " if l != 5 else ""))
                    m = Minion(rnd["attack"], rnd["health"], lineup=side)
                    if rnd.get("mechanics") is not None:
                        if "TAUNT" in rnd.get("mechanics"):
                            m.add_effect(Taunt)
                        if "DIVINE_SHIELD" in rnd.get("mechanics"):
                            m.add_effect(DivineShield)
                        if "POISONOUS" in rnd.get("mechanics"):
                            m.add_effect(Poison)

                    side.append(m)
                anal.lineups.write("\n")

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
