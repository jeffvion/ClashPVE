from game.units.base import Unit


class Skeleton(Unit):
    """Rapide, fragile, sort en groupe."""

    name = "Squelette"
    max_hp = 40
    damage = 12
    speed = 95.0
    attack_range = 18
    attack_cooldown = 0.8
    radius = 8
    color = (230, 230, 220)
