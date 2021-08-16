from typing import Optional, Type, List
from random import randint

from effect import Effect, Poison, Taunt, DivineShield


class Minion:
    """ A Unit of a lineup. Defined by its health, damage and its effects. """
    def __init__(self, attack: int = 1, health: int = 1, lineup: Optional['Lineup'] = None):
        """
        :param attack: Base attack of the minion
        :param health: Base health of the minion
        :param lineup: Which lineup this Minion belongs to (used for effects and printing)
        """
        self.attack = attack
        self.health = health
        self.lineup = lineup

        self.effects: List[Effect] = []

        self.has_attacked = False

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
        if randint(0, 100) < 25:
            m.effects.append(Poison(m))
        if randint(0, 100) < 50:
            m.effects.append(Taunt(m))

        return m

    def dead(self) -> bool:
        """ is my health below zero? """
        return self.health <= 0

    def has_effect(self, effect_type: Type[Effect]) -> bool:
        """ Does this minion have an effect with this type? """
        return len([e for e in self.effects if isinstance(e, effect_type)]) > 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        """ The string representation of this minion. """
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

        return f"""{shell_color}[{endc}{attack}{endc}{shell_color}|{endc}{health}{endc}{shell_color}]{endc}"""


class Lineup(List[Minion]):
    """ A List of minions. """
    def __init__(self, color: str):
        self.color = color
        super().__init__()

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
