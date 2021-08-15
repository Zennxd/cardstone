Minion: str = "Minion"


class Effect:
    def __init__(self, owner: Minion):
        self.owner = owner

    def before_attack(self, target: Minion):
        pass

    def after_attack(self, target: Minion):
        pass

    def combat_start(self):
        pass

    def on_damage(self, attacker: Minion):
        pass

    def on_death(self, attacker: Minion):
        pass


class Taunt(Effect):
    # implementation in Lineup.random_minion()
    pass


class DivineShield(Effect):
    # implementation in Battleground.one_step
    pass


class Poison(Effect):
    def after_attack(self, target: Minion):
        target.health = -999999
