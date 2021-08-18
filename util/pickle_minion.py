from pickle import dumps
from minion import Minion
from effect import Taunt, AOE, DivineShield, Poison

# create minion
m = Minion(2, 4, None)
m.effects.append(AOE(m))


with open("../minions/hydra.minion", "bw+") as file:
    file.write(dumps(m))
