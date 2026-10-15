import pygame
from game.settings import BLACK, WHITE, RED, TEAM_PLAYER


class Unit:
    """Unite generique : se deplace vers la cible la plus proche et attaque."""

    name = "Unit"
    max_hp = 100
    damage = 10
    speed = 60.0          # pixels / seconde
    attack_range = 25     # pixels
    attack_cooldown = 1.0  # secondes
    radius = 10
    color = (200, 200, 200)

    def __init__(self, pos, team):
        self.pos = pygame.Vector2(pos)
        self.team = team
        self.hp = self.max_hp
        self._cooldown = 0.0
        self.target = None

    @property
    def alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    # --- Ciblage ---
    def _distance_to(self, other):
        return self.pos.distance_to(other.pos) - getattr(other, "radius", 0)

    def acquire_target(self, enemy_units, enemy_castle):
        candidates = [u for u in enemy_units if u.alive]
        if enemy_castle.alive:
            candidates.append(enemy_castle)
        if not candidates:
            self.target = None
            return
        self.target = min(candidates, key=self._distance_to)

    # --- Mise a jour ---
    def update(self, dt, enemy_units, enemy_castle):
        self._cooldown = max(0.0, self._cooldown - dt)
        self.acquire_target(enemy_units, enemy_castle)
        if self.target is None:
            return

        dist = self._distance_to(self.target)
        if dist <= self.attack_range:
            if self._cooldown == 0.0:
                self.target.take_damage(self.damage)
                self._cooldown = self.attack_cooldown
        else:
            direction = self.target.pos - self.pos
            if direction.length() > 0:
                self.pos += direction.normalize() * self.speed * dt

    # --- Affichage ---
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
        outline = (50, 90, 200) if self.team == TEAM_PLAYER else RED
        pygame.draw.circle(surface, outline, self.pos, self.radius, 3)
        # Barre de vie
        w = self.radius * 2
        x = self.pos.x - self.radius
        y = self.pos.y - self.radius - 8
        pygame.draw.rect(surface, BLACK, (x, y, w, 4))
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, WHITE, (x, y, int(w * ratio), 4))
