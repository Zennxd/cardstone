from typing import Optional, Type, List
from random import randint

from effect import Effect, Poison, Taunt, DivineShield


class Minion:
    def __init__(self, attack: int = 1, health: int = 1, lineup: Optional['Lineup'] = None):
        self.attack = attack
        self.health = health
        self.lineup = lineup

        self.effects: List[Effect] = []

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

    def has_effect(self, effect_type: Type[Effect]) -> bool:
        return len([e for e in self.effects if isinstance(e, effect_type)]) > 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        endc: str = "\033[0m"
        shell_color: str = self.lineup.color
        if self.has_effect(Taunt):
            shell_color += '\033[4m'  # underlined

        attack: str = str(self.attack).rjust(2)
        poison: str = '\033[92m'  # green
        if self.has_effect(Poison):
            attack = f"{poison}{attack}"

        health: str = str(self.health).rjust(2)
        if self.health < 1:
            health = f"\033[91m{health}"  # red

        return f"""{shell_color}[{endc}{attack}{endc}|{health}{endc}{shell_color}]{endc}"""


class Lineup(List[Minion]):
    def __init__(self, color: str):
        self.color = color
        super().__init__()

    def random_target(self) -> Minion:
        taunts = [t for t in self if t.has_effect(Taunt)]
        if len(taunts) > 0:
            return taunts[randint(0, len(taunts) - 1)]

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
