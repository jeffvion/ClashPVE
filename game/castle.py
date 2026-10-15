import pygame
from game.settings import (
    CASTLE_HP, CASTLE_SIZE, WIDTH, HEIGHT, BLUE, RED, WHITE, BLACK,
    TEAM_PLAYER,
)


class Castle:
    def __init__(self, team):
        self.team = team
        self.max_hp = CASTLE_HP
        self.hp = CASTLE_HP
        w, h = CASTLE_SIZE
        x = WIDTH // 2
        y = HEIGHT - 70 if team == TEAM_PLAYER else 70
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)
        self.radius = w // 2

    @property
    def alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def draw(self, surface):
        color = BLUE if self.team == TEAM_PLAYER else RED
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=8)
        # Barre de vie
        bar = pygame.Rect(self.rect.x, self.rect.y - 14, self.rect.width, 8)
        pygame.draw.rect(surface, BLACK, bar)
        ratio = self.hp / self.max_hp
        inner = bar.copy()
        inner.width = int(bar.width * ratio)
        pygame.draw.rect(surface, WHITE if ratio > 0.3 else RED, inner)
