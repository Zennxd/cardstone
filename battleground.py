from typing import List
from enum import IntEnum
import random

from minion import Minion, Lineup


class Order(IntEnum):
    """ Sets which side starts attacking in a fight."""
    NORTH_FIRST = 0,
    """ North attacks first in the fight """
    SOUTH_FIRST = 1
    """ South attacks first in the fight """


class Battleground:
    step: int = 0
    """ Which attack of the fight we're currently simulating
        (or: after the fight is over, the amount of attacks)"""

    order: Order = Order.NORTH_FIRST
    """ Whether the first or second lineup attacks first """

    north_side: Lineup = Lineup(color='\033[94m')
    """ First lineup of the fight, drawn at the top"""
    south_side: Lineup = Lineup(color='\033[93m')

    @classmethod
    def sides(cls):
        yield cls.north_side
        yield cls.south_side

    @classmethod
    def clear_sides(cls) -> None:
        for side in cls.sides():
            side.clear()

    @classmethod
    def reset(cls):
        cls.clear_sides()
        cls.step = 0

    @classmethod
    def next_attacking_side(cls) -> Lineup:
        """ this returns the opposite of next_target_side for a given step.
         the cls.order offsets the order by one if set to SOUTH_FIRST. """
        return cls.north_side if (cls.step + cls.order) % 2 == 0 else cls.south_side

    @classmethod
    def next_target_side(cls) -> Lineup:
        """ this returns the opposite of next_attacking_side for a given step.
                 the cls.order offsets the order by one if set to SOUTH_FIRST. """
        return cls.north_side if (cls.step + cls.order) % 2 == 1 else cls.south_side

    @classmethod
    def one_step(cls):
        """ The main logic for a given step in a fight. This method calls minion effects, calculates minion damage
         during and after the attack, and prints the attack's outcome.
         This method also increments the step variable. """
        for m in cls.north_side + cls.south_side:
            for effect in m.effects:
                effect.combat_start()

        # select next attacker
        attacking_side = cls.next_attacking_side()
        attacker: Minion = attacking_side.next_attacker()

        # choose random target
        target: Minion = cls.next_target_side().random_target()

        print(f"{attacker} attacks {target} -> ", end="")

        for effect in attacker.effects:
            effect.before_attack(target)

        target.health -= attacker.attack
        attacker.health -= target.attack

        for effect in target.effects:
            effect.on_damage(attacker)
            if target.dead():
                effect.on_death(attacker)

        for effect in attacker.effects:
            effect.after_attack(target)

        print(f"{attacker}  {target}")

        attacker.has_attacked = True

        for side in [cls.north_side, cls.south_side]:
            for m in side:
                if m.dead():
                    side.remove(m)

        cls.step += 1
        print("")

    @classmethod
    def render(cls):
        """ Print the state of both north and south. This mostly depends on Minion.__repr__. """
        print(f"step: {cls.step if cls.step != 0 else 'Initial'}")
        for i, side in enumerate([cls.north_side, cls.south_side]):
            for m in side:
                print(f"  {m}  ", end="")
            print("")
        print("")

    @classmethod
    def fight(cls):
        """ call one_step until the fight is over.
            A fight is over if one or both lineups are defeated (e.g. empty). """
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

        # main logic/view loop
        while not cls.north_side.defeated() and not cls.south_side.defeated():
            cls.one_step()
            cls.render()
