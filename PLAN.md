# ClashPVE : plan détaillé

Objectif : un jeu Python avec interface, équivalent de Clash Royale, où le joueur affronte une IA qui contrôle des châteaux et des monstres (squelettes, zombies).

## État actuel

- Squelette du projet en place (arène, cartes, unités, IA, boucle de jeu).
- Phase 1 poussée partiellement : `game/arena.py` et `game/units/base.py` réécrits (waypoints par lane, états `marche` / `combat`, aggro).
- **À finir pour la phase 1** : adapter `game.py`, `cards.py`, `ai.py`, `units/skeleton.py`, `units/zombie.py` à la nouvelle signature `Unit(x, y, team, arena, enemy_castle_pos)`.

## Phase 1 : déplacement et combat des unités

- Chemins par lane : entrée du pont, sortie du pont, château adverse.
- État `marche` : l'unité suit ses waypoints.
- État `combat` : une unité quitte son chemin si un ennemi entre dans sa portée d'aggro.
- Reprise du chemin au prochain waypoint devant l'unité après le combat.
- Pas de combat depuis l'eau (hors pont).
- Validation : une unité posée sur une lane traverse le pont, attaque les ennemis rencontrés, puis atteint le château.

## Phase 2 : châteaux, tours et conditions de victoire

- Château principal et 2 tours de défense par camp, avec points de vie.
- Les tours tirent sur les unités à portée.
- Couronnes : une tour détruite donne une couronne à l'adversaire.
- Destruction du château principal : victoire immédiate.
- Chronomètre de 3 minutes ; au terme, victoire au nombre de couronnes.
- Prolongation avec élixir double, puis mort subite en cas d'égalité.
- Validation : une partie complète se termine par victoire, défaite ou égalité résolue.

## Phase 3 : élixir, cartes et main du joueur

- Jauge d'élixir (max 10), régénération continue, double en prolongation.
- Deck de cartes, main de 4 cartes, file de rotation.
- Chaque carte a un coût et fait apparaître une ou plusieurs unités.
- Placement limité à la moitié de terrain du joueur.
- Validation : on ne peut pas jouer une carte sans élixir suffisant ; la main se renouvelle.

## Phase 4 : IA adverse

- L'IA gère sa propre jauge d'élixir et son deck.
- Choix de lane selon la pression ennemie et ses défenses.
- Contre-attaque après avoir défendu, avec réserve d'élixir minimale.
- Niveaux de difficulté : facile, normal, difficile (délai de réaction, qualité des choix).
- Validation : l'IA joue des cartes régulièrement et réagit aux attaques du joueur.

## Phase 5 : contenu (monstres et équilibrage)

- Unités de base : squelette, zombie.
- Nouvelles unités : escouade de squelettes, géant zombie, archer squelette, nécromancien.
- Un fichier de configuration central pour les statistiques (PV, dégâts, vitesse, portée, coût).
- Passage d'équilibrage sur coûts et statistiques.

## Phase 6 : interface et rendu

- Menu principal, écran de partie, écran de fin.
- Affichage : arène, barres de vie, jauge d'élixir, main de cartes, chronomètre, couronnes.
- Sprites et animations simples (marche, attaque, mort).
- Effets sonores et musique.

## Phase 7 : finition

- Sauvegarde des réglages et des statistiques de parties.
- Tests automatisés sur la logique (combat, élixir, victoire).
- README avec instructions d'installation et de lancement.
- Packaging (exécutable ou script de lancement).

## Ordre recommandé

1. Finir la phase 1 (adapter les fichiers restants).
2. Phases 2 et 3 (tours, victoire, élixir, cartes).
3. Phase 4 (IA).
4. Phases 5 et 6 (contenu et interface).
5. Phase 7 (finition).
