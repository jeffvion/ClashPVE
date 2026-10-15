"""Classe de base des unites: marche par waypoints, aggro, combat."""
import math
import pygame

WALK = "marche"
FIGHT = "combat"


class Unit:
    name = "Unit"
    max_hp = 100
    damage = 10
    attack_range = 25
    attack_cooldown = 1.0
    speed = 50
    aggro_range = 90
    radius = 10
    color = (200, 200, 200)

    def __init__(self, x, y, team, arena, enemy_castle_pos):
        self.pos = pygame.Vector2(x, y)
        self.team = team
        self.arena = arena
        self.hp = self.max_hp
        self.cooldown = 0.0
        self.state = WALK
        self.target = None
        lane = arena.lane_of(x)
        self.waypoints = arena.waypoints(lane, team, enemy_castle_pos)
        self.wp_index = self._closest_forward_waypoint()

    # ---------- helpers ----------
    @property
    def alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def _dir_sign(self):
        return -1 if self.team == "player" else 1

    def _closest_forward_waypoint(self):
        """Premier waypoint encore devant l'unite (dans le sens de marche)."""
        s = self._dir_sign()
        for i, (_, wy) in enumerate(self.waypoints[:-1]):
            if (wy - self.pos.y) * s > 0:
                return i
        return len(self.waypoints) - 1

    def _dist(self, other):
        return self.pos.distance_to(other.pos)

    def _find_target(self, enemies, castle):
        best, best_d = None, self.aggro_range
        for e in enemies:
            if e.alive:
                d = self._dist(e)
                if d < best_d:
                    best, best_d = e, d
        if best:
            return best
        if castle.alive and self._dist(castle) < self.aggro_range + castle.radius:
            return castle
        return None

    def _move_towards(self, point, dt):
        vec = pygame.Vector2(point) - self.pos
        dist = vec.length()
        if dist < 1e-3:
            return True
        step = self.speed * dt
        if step >= dist:
            self.pos.update(point)
            return True
        self.pos += vec / dist * step
        return False

    # ---------- update ----------
    def update(self, dt, enemies, enemy_castle):
        self.cooldown = max(0.0, self.cooldown - dt)

        # Pas de combat/aggro tant qu'on est engage dans la riviere hors pont.
        target = self._find_target(enemies, enemy_castle)
        if target is not None and not (self.arena.in_river(self.pos) and not self.arena.on_bridge(self.pos)):
            self.target = target
            self.state = FIGHT
        else:
            if self.state == FIGHT:
                # reprise du chemin au waypoint le plus proche devant nous
                self.wp_index = self._closest_forward_waypoint()
            self.target = None
            self.state = WALK

        if self.state == FIGHT:
            self._fight(dt)
        else:
            self._walk(dt)

    def _walk(self, dt):
        if self.wp_index >= len(self.waypoints):
            return
        if self._move_towards(self.waypoints[self.wp_index], dt):
            self.wp_index = min(self.wp_index + 1, len(self.waypoints) - 1)

    def _fight(self, dt):
        t = self.target
        reach = self.attack_range + getattr(t, "radius", 0)
        if self._dist(t) > reach:
            self._move_towards(t.pos, dt)
        elif self.cooldown <= 0:
            t.take_damage(self.damage)
            self.cooldown = self.attack_cooldown

    # ---------- draw ----------
    def draw(self, surf):
        col = self.color if self.team == "player" else tuple(min(255, c + 40) for c in (200, 60, 60))
        pygame.draw.circle(surf, col, (int(self.pos.x), int(self.pos.y)), self.radius)
        w = 20
        ratio = self.hp / self.max_hp
        bar = pygame.Rect(int(self.pos.x) - w // 2, int(self.pos.y) - self.radius - 8, w, 4)
        pygame.draw.rect(surf, (80, 0, 0), bar)
        pygame.draw.rect(surf, (0, 200, 0), (bar.x, bar.y, int(w * ratio), 4))
