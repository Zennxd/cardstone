from types import MethodType
from dill import dumps
from effect import Effect, Taunt
from minion import Minion


# create admiral (+1/+1 for every attack it survives)
m = Minion(9, 10, None)
m.add_effect(Taunt)

class CustomEffect(Effect):
    def on_damage(self, attacker: Minion):
        print("admiral casts +1/+1 on entire lineup")
        for minion in self.owner.lineup:
            minion.attack += 1
            minion.health += 1


custom_effect = CustomEffect(m)
m.effects.append(custom_effect)

with open("../minions/admiral.minion", "bw+") as file:
    file.write(dumps(m))
