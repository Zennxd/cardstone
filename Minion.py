from typing import Optional, Type, List
from random import randint

import Effect


class Minion:
    def __init__(self, attack: int = 1, health: int = 1, lineup: Optional['Lineup'] = None):
        self.attack = attack
        self.health = health
        self.lineup = lineup

        self.has_attacked = False

    @classmethod
    def default_minion(cls, lineup: 'Lineup') -> 'Minion':
        return Minion(
            attack=randint(1, 4),
            health=randint(1, 8),
            lineup=lineup
        )

    @classmethod
    def elite_minion(cls, lineup: 'Lineup') -> 'Minion':
        return Minion(
            attack=randint(5, 30),
            health=randint(1, 25),
            lineup=lineup
        )

    def dead(self) -> bool:
        return self.health <= 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"""{self.lineup.color}[{str(self.attack).rjust(2)}|{str(self.health).rjust(2)}]\033[0m"""


class Lineup(List[Minion]):
    def __init__(self, color: str):
        self.color = color
        super().__init__()

    def random_minion(self) -> Minion:
        return self[randint(0, len(self) - 1)]

    def next_attacker(self) -> Minion:
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
        return len(self) < 1
