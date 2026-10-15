# ClashPVE

Jeu de stratégie en Python (Pygame) inspiré de Clash Royale, mais en **PVE** : on affronte une IA qui contrôle un château et des monstres (squelettes, zombies).

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Contrôles

- Touches `1` / `2` : sélectionner la carte (Squelettes / Zombie)
- Clic gauche dans votre moitié de l'arène (en bas) : poser l'unité
- `Échap` : quitter

## Structure

```
main.py            point d'entrée
game/settings.py   constantes
game/arena.py      terrain
game/castle.py     châteaux
game/elixir.py     ressource élixir
game/cards.py      cartes
game/ai.py         adversaire IA
game/units/        unités (Unit, Skeleton, Zombie)
game/game.py       boucle de jeu et logique
```

## Idées pour la suite

- Sprites et sons
- Tours de défense, deux lanes avec pont
- IA réactive puis niveaux de difficulté
- Menus (accueil, fin de partie)
