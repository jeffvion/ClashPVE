import sys
import random
import pygame

from game.settings import (
    WIDTH, HEIGHT, FPS, WHITE, BLACK, PURPLE, TEAM_PLAYER, ELIXIR_MAX,
)
from game.arena import Arena
from game.castle import Castle
from game.elixir import Elixir
from game.cards import DECK
from game.ai import AIPlayer


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ClashPVE")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.big_font = pygame.font.SysFont("arial", 48, bold=True)
        self.reset()

    def reset(self):
        self.arena = Arena()
        self.player_castle = Castle(TEAM_PLAYER)
        self.ai_castle = Castle("ai")
        self.player_units = []
        self.ai_units = []
        self.elixir = Elixir()
        self.ai = AIPlayer()
        self.selected = 0
        self.winner = None

    # --- Evenements ---
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_r and self.winner:
                    self.reset()
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    idx = event.key - pygame.K_1
                    if idx < len(DECK):
                        self.selected = idx
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.winner:
                    self.try_deploy(event.pos)

    def try_deploy(self, pos):
        card = DECK[self.selected]
        if not self.arena.is_in_team_half(pos, TEAM_PLAYER):
            return
        if not self.elixir.spend(card.cost):
            return
        for _ in range(card.count):
            offset = pygame.Vector2(random.randint(-20, 20), random.randint(-20, 20))
            self.player_units.append(
                card.factory(pygame.Vector2(pos) + offset, TEAM_PLAYER)
            )

    # --- Logique ---
    def update(self, dt):
        if self.winner:
            return
        self.elixir.update(dt)
        self.ai.update(dt, self)

        for u in self.player_units:
            u.update(dt, self.ai_units, self.ai_castle)
        for u in self.ai_units:
            u.update(dt, self.player_units, self.player_castle)

        self.player_units = [u for u in self.player_units if u.alive]
        self.ai_units = [u for u in self.ai_units if u.alive]

        if not self.ai_castle.alive:
            self.winner = "Victoire !"
        elif not self.player_castle.alive:
            self.winner = "Defaite..."

    # --- Affichage ---
    def draw(self):
        self.arena.draw(self.screen)
        self.ai_castle.draw(self.screen)
        self.player_castle.draw(self.screen)
        for u in self.ai_units + self.player_units:
            u.draw(self.screen)
        self.draw_hud()
        if self.winner:
            self.draw_end_screen()
        pygame.display.flip()

    def draw_hud(self):
        # Barre d'elixir
        bar = pygame.Rect(10, HEIGHT - 28, WIDTH - 20, 16)
        pygame.draw.rect(self.screen, BLACK, bar, border_radius=6)
        inner = bar.copy()
        inner.width = int(bar.width * self.elixir.amount / ELIXIR_MAX)
        pygame.draw.rect(self.screen, PURPLE, inner, border_radius=6)
        txt = self.font.render(f"Elixir {int(self.elixir.amount)}", True, WHITE)
        self.screen.blit(txt, (14, HEIGHT - 52))
        # Cartes
        for i, card in enumerate(DECK):
            color = (255, 220, 80) if i == self.selected else WHITE
            label = self.font.render(
                f"[{i + 1}] {card.name} ({card.cost})", True, color
            )
            self.screen.blit(label, (150 + i * 170, HEIGHT - 52))

    def draw_end_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        text = self.big_font.render(self.winner, True, WHITE)
        self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        hint = self.font.render("R : rejouer   Echap : quitter", True, WHITE)
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    # --- Boucle principale ---
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()
