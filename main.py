from random import randint
from battleground import Battleground
from Minion import Minion
from effect import Poison, Taunt


if __name__ == "__main__":
    for side in [Battleground.north_side, Battleground.south_side]:
        for i in range(0, randint(5, 7)):
            side.append(
                Minion.default_minion(side) if randint(1, 100) > 30 else Minion.elite_minion(side)
            )
        for m in side:
            if randint(0, 100) < 10:
                m.effects.append(Poison(m))
            if randint(0, 100) < 30:
                m.effects.append(Taunt(m))

    Battleground.fight()

    if Battleground.north_side.defeated() and Battleground.south_side.defeated():
        print("Draw")
    elif not Battleground.north_side.defeated() and Battleground.south_side.defeated():
        print("North won")
    else:
        print("South won")

    print("attacks: " + str(Battleground.step))
