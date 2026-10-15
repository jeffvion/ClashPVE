import random
import pygame

from game.elixir import Elixir
from game.cards import DECK
from game.settings import WIDTH, TEAM_AI


class AIPlayer:
    """Adversaire IA (version simple).

    Etape 1 : pose une carte aleatoire des qu'il a assez d'elixir.
    A ameliorer : contrer les unites du joueur, choisir la lane, difficulte.
    """

    def __init__(self, think_delay=(2.0, 4.0)):
        self.elixir = Elixir()
        self.think_delay = think_delay
        self._timer = random.uniform(*think_delay)

    def update(self, dt, game):
        self.elixir.update(dt)
        self._timer -= dt
        if self._timer > 0:
            return
        self._timer = random.uniform(*self.think_delay)

        affordable = [c for c in DECK if self.elixir.can_afford(c.cost)]
        if not affordable:
            return
        card = random.choice(affordable)
        self.elixir.spend(card.cost)
        lane_x = random.choice((WIDTH // 4, 3 * WIDTH // 4))
        for i in range(card.count):
            offset = pygame.Vector2(random.randint(-20, 20), random.randint(0, 20))
            pos = pygame.Vector2(lane_x, 150) + offset
            game.ai_units.append(card.factory(pos, TEAM_AI))
