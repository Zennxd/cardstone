from random import randint
from battleground import Battleground
from minion import Minion
from effect import Poison, Taunt


if __name__ == "__main__":
    # fill both teams
    for side in [Battleground.north_side, Battleground.south_side]:
        for i in range(0, randint(5, 7)):
            side.append(
                Minion.default_minion(side) if randint(1, 100) > 50 else Minion.elite_minion(side)
            )
        # for m in side:
        #     m.effects.append(Poison(m))

    # fight! (this calls what is essentially the main loop of the application)
    Battleground.fight()

    # evaluate
    if Battleground.north_side.defeated() and Battleground.south_side.defeated():
        print("Draw")
    elif not Battleground.north_side.defeated() and Battleground.south_side.defeated():
        print("North won")
    else:
        print("South won")

    print("attacks: " + str(Battleground.step))
