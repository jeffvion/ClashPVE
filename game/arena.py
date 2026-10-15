"""Terrain: riviere, ponts et waypoints par lane."""
import pygame
from . import settings as S

LANES = ("left", "right")


class Arena:
    def __init__(self):
        self.width = S.WIDTH
        self.height = S.HEIGHT
        self.river_y = self.height // 2
        self.river_h = 40
        self.bridge_w = 70
        self.lane_x = {"left": self.width // 4, "right": 3 * self.width // 4}
        self.bridges = {
            lane: pygame.Rect(x - self.bridge_w // 2, self.river_y - self.river_h // 2,
                              self.bridge_w, self.river_h)
            for lane, x in self.lane_x.items()
        }

    def lane_of(self, x):
        """Lane la plus proche d'une coordonnee x."""
        return "left" if abs(x - self.lane_x["left"]) <= abs(x - self.lane_x["right"]) else "right"

    def waypoints(self, lane, team, target_pos):
        """Chemin: entree du pont, sortie du pont, puis cible finale.

        team 'player' monte (y diminue), team 'ai' descend (y augmente).
        """
        x = self.lane_x[lane]
        top = self.river_y - self.river_h // 2 - 5
        bottom = self.river_y + self.river_h // 2 + 5
        if team == "player":
            pts = [(x, bottom), (x, top)]
        else:
            pts = [(x, top), (x, bottom)]
        pts.append((float(target_pos[0]), float(target_pos[1])))
        return pts

    def in_river(self, pos):
        return abs(pos[1] - self.river_y) < self.river_h // 2

    def on_bridge(self, pos):
        return any(b.collidepoint(pos) for b in self.bridges.values())

    def side_of(self, y):
        return "ai" if y < self.river_y else "player"

    def draw(self, surf):
        surf.fill((70, 140, 70))
        river = pygame.Rect(0, self.river_y - self.river_h // 2, self.width, self.river_h)
        pygame.draw.rect(surf, (60, 110, 200), river)
        for b in self.bridges.values():
            pygame.draw.rect(surf, (140, 100, 60), b)
