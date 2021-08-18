import math
import numbers
from typing import Optional, Type, List
from random import randint

import colorama

from effect import *

from colorama import Fore


class Minion:
    """ A Unit of a lineup. Defined by its health, damage and its effects. """
    def __init__(self, attack: int = 1, health: int = 1, lineup: Optional['Lineup'] = None):
        """
        :param attack: Base attack of the minion
        :param health: Base health of the minion
        :param lineup: Which lineup this Minion belongs to (used for effects and printing)
        """
        self._attack = attack
        self._health = health
        self.lineup = lineup

        self.effects: List[Effect] = []

        self.has_attacked = False

    @property
    def attack(self):
        return self._attack if not self.has_effect(Poison) else math.inf

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < self._health and self.has_effect(DivineShield):
            self.effects = [e for e in self.effects if not isinstance(e, DivineShield)]
        else:
            self._health = value

    @property
    def place(self) -> int:
        """ returns the minions place in its lineup, or -1 if no lineup exists """
        if self.lineup is None:
            return -1
        return [i for i, m in enumerate(self.lineup) if m is self][0]

    # attacking
    def attack_minion(self, target: 'Minion'):
        """ In what way this minion attacks """
        target.health -= self.attack

    # util
    def add_effect(self, effect_type: Type[Effect]) -> None:
        """ Adds an instance of given Effect type to self. """
        self.effects.append(effect_type(self))

    def dead(self) -> bool:
        """ is my health zero or below? """
        return self.health < 1

    def has_effect(self, effect_type: Type[Effect]) -> bool:
        """ Does this minion have an effect with this type? """
        return len([e for e in self.effects if isinstance(e, effect_type)]) > 0

    # factories
    @classmethod
    def default_minion(cls, lineup: 'Lineup') -> 'Minion':
        """ Factory method: returns a random, smol minion """
        return Minion(
            attack=randint(1, 4),
            health=randint(1, 8),
            lineup=lineup
        )

    @classmethod
    def elite_minion(cls, lineup: 'Lineup') -> 'Minion':
        """ Factory method: returns a random, big minion (with potential effects) """
        m = Minion(
            attack=randint(5, 30),
            health=randint(1, 25),
            lineup=lineup
        )
        for e in [DivineShield, Poison]:
            if randint(0, 100) < 25:
                m.add_effect(e)

        return m

    # protocols
    def __str__(self):
        """ The string representation of this minion. """
        spacing: str = " "
        endc: str = "\033[0m"
        poison: str = '\033[92m'  # green
        shell_color: str = self.lineup.color if not self.has_effect(DivineShield) else Fore.YELLOW

        if self.has_effect(Taunt):
            shell_color += '\033[4m'  # underlined

        attack: str = str(self.attack).rjust(3, spacing)
        if self.has_effect(Poison):
            attack = f"{poison}{attack}"

        health: str = str(self.health).rjust(3, spacing)
        if self.health < 1:
            health = f"\033[91m{health}"  # red

        return f"""{self.place}.{shell_color}[{endc}{attack}{endc}{shell_color}|{endc}{health}{endc}{shell_color}]{endc}"""

    def __repr__(self):
        repr_str: str = "Minion "
        repr_str += f"Attack={self.attack} Health={self.health} "
        repr_str += f"Place: {self.lineup.index(self)}" if self.lineup is not None else ""

        return repr_str


class Lineup(List[Minion]):
    """ A List of minions. """
    def __init__(self, color: str):
        self.color = color
        super().__init__()

    def before_of(self, m: Minion) -> Minion:
        idx: int = m.place
        return self[idx - 1] if idx != 0 else None

    def next_of(self, m: Minion) -> Minion:
        idx: int = m.place
        return self[idx + 1] if idx != len(self)-1 else None

    def random_target(self) -> Minion:
        """ Returns a random target for an attack.
            The Taunt effect's functionality is implemented here. """
        taunts = [t for t in self if t.has_effect(Taunt)]
        if len(taunts) > 0:
            return taunts[randint(0, len(taunts) - 1)]

        return self[randint(0, len(self) - 1)]

    def next_attacker(self) -> Minion:
        """ returns the next attacker of this lineup.
            The usual order rules are applied. """
        attacker: Optional[Minion] = None

        can_attack = [m for m in self if not m.has_attacked]
        # if no one can attack, reset all attack flags
        if len(can_attack) == 0:
            for m in self:
                m.has_attacked = False
            attacker = self[0]
        else:
            attacker = can_attack[0]

        return attacker

    def defeated(self):
        """ Is everyone dead? """
        return len(self) < 1
