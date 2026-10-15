from dataclasses import dataclass
from typing import Callable

from game.units.skeleton import Skeleton
from game.units.zombie import Zombie


@dataclass
class Card:
    name: str
    cost: int
    count: int  # nombre d'unites posees
    factory: Callable  # factory(pos, team) -> Unit


SKELETONS = Card("Squelettes", 3, 3, Skeleton)
ZOMBIE = Card("Zombie", 4, 1, Zombie)

DECK = [SKELETONS, ZOMBIE]
