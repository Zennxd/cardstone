from typing import Optional
from enum import IntEnum
import random

from minion import Minion, Lineup


class Order(IntEnum):
    NORTH_FIRST = 0,
    SOUTH_FIRST = 1


class Battleground:
    north_side: Lineup = Lineup('\033[94m')
    south_side: Lineup = Lineup('\033[93m')

    step: int = 0

    order: Order = Order.NORTH_FIRST

    @classmethod
    def next_attacking_side(cls) -> Lineup:
        return cls.north_side if (cls.step + cls.order) % 2 == 0 else cls.south_side

    @classmethod
    def next_target_side(cls) -> Lineup:
        return cls.north_side if (cls.step + cls.order) % 2 == 1 else cls.south_side

    @classmethod
    def one_step(cls):
        # select next attacker
        attacking_side = cls.next_attacking_side()
        attacker: Minion = attacking_side.next_attacker()

        # choose random target
        target: Minion = cls.next_target_side().random_minion()

        print(f"{attacker} attacks {target} -> ", end="")

        target.health -= attacker.attack
        attacker.health -= target.attack

        print(f"{attacker}  {target}")

        attacker.has_attacked = True

        for m in [attacker, target]:
            if m.dead() and m.lineup is not None:
                m.lineup.remove(m)

        cls.step += 1
        print("")

    @classmethod
    def render(cls):
        print(f"step: {cls.step if cls.step != 0 else 'Initial'}")
        for i, side in enumerate([cls.north_side, cls.south_side]):
            for m in side:
                print(f"  {m}  ", end="")
            print("")
        print("")

    @classmethod
    def fight(cls):
        if len(cls.north_side) > len(cls.south_side):
            print("North attacks first")
            cls.order = Order.NORTH_FIRST
        elif len(cls.north_side) < len(cls.south_side):
            print("South attacks first")
            cls.order = Order.SOUTH_FIRST
        else:
            order: int = random.randint(0, 1)
            print(f"Random order, {'North' if order == Order.NORTH_FIRST else 'South'} attacks first")
            cls.order = Order(order)

        cls.render()

        while not cls.north_side.defeated() and not cls.south_side.defeated():
            cls.one_step()
            cls.render()
