from game.settings import ELIXIR_MAX, ELIXIR_START, ELIXIR_PER_SECOND


class Elixir:
    def __init__(self, rate=ELIXIR_PER_SECOND):
        self.amount = float(ELIXIR_START)
        self.rate = rate

    def update(self, dt):
        self.amount = min(ELIXIR_MAX, self.amount + self.rate * dt)

    def can_afford(self, cost):
        return self.amount >= cost

    def spend(self, cost):
        if not self.can_afford(cost):
            return False
        self.amount -= cost
        return True
