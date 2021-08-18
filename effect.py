Minion: str = "Minion"  # circulatory import prevention bear ʕ •ᴥ•ʔ


class Effect:
    """ An Effect is a special property of a minion, such as killing instantly with every attack (Poison)
        or not taking damage for one attack (DivineShield). Below (after __init__) are the event hooks that
        can be overriden in each Effect definition. """
    def __init__(self, owner: Minion):
        self.owner = owner

    def before_attack(self, target: Minion):
        """ Triggered just before a minion attacks. """
        pass

    def after_attack(self, target: Minion):
        """ Triggered just after a minion attacks (no matter if it dies or not) """
        pass

    def combat_start(self):
        """ triggered at the start of step 0. """
        pass

    def on_damage(self, attacker: Minion):
        """ triggered when this minion takes damage, but doesn't die. """
        pass

    def on_death(self, attacker: Minion):
        """ triggered when a minion takes lethal damage. """
        pass


class Taunt(Effect):
    """ An enemy minion must choose a minion with Taunt for an attack, if any exist """
    # implementation in Lineup.random_target()
    pass


class DivineShield(Effect):
    """ A minion will not lose health for an attack if it has a Divine Shield. """
    # implementation in Minion.health.setter
    pass


class Poison(Effect):
    """ The target of an attack by this minion will take practically infinite damage """
    def after_attack(self, target: Minion):
        target.health = -999

    def on_damage(self, attacker: Minion):
        attacker.health = -999


class AOE(Effect):
    """ Area- Of- Effect deals damage to the minions next to the target. """
    def after_attack(self, target: Minion):
        left: Minion = target.lineup.before_of(target)
        right: Minion = target.lineup.next_of(target)

        for m in [left, right]:
            if m is not None:
                m.health -= self.owner.attack
