import pygame
from game.settings import (
    WIDTH, HEIGHT, GREEN, DARK_GREEN, RIVER, BRIDGE, RIVER_Y, RIVER_HEIGHT,
)


class Arena:
    """Terrain de jeu : herbe, riviere et deux ponts."""

    BRIDGE_XS = (WIDTH // 4, 3 * WIDTH // 4)
    BRIDGE_WIDTH = 60

    def draw(self, surface):
        surface.fill(GREEN)
        # Damier leger pour le style
        for y in range(0, HEIGHT, 80):
            pygame.draw.rect(surface, DARK_GREEN, (0, y, WIDTH, 40))
        # Riviere
        pygame.draw.rect(
            surface, RIVER, (0, RIVER_Y - RIVER_HEIGHT // 2, WIDTH, RIVER_HEIGHT)
        )
        # Ponts
        for bx in self.BRIDGE_XS:
            pygame.draw.rect(
                surface,
                BRIDGE,
                (bx - self.BRIDGE_WIDTH // 2, RIVER_Y - RIVER_HEIGHT // 2,
                 self.BRIDGE_WIDTH, RIVER_HEIGHT),
            )

    def is_in_team_half(self, pos, team):
        """Le joueur ne peut poser des unites que dans sa moitie (en bas)."""
        _, y = pos
        if team == "player":
            return y > RIVER_Y + RIVER_HEIGHT // 2
        return y < RIVER_Y - RIVER_HEIGHT // 2
