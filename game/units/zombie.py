from game.units.base import Unit


class Zombie(Unit):
    """Lent, beaucoup de PV, gros degats."""

    name = "Zombie"
    max_hp = 260
    damage = 30
    speed = 40.0
    attack_range = 22
    attack_cooldown = 1.2
    radius = 14
    color = (90, 160, 90)
