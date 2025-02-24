# Battleships
Overview:

This is a two-player Battleship game built with Pygame. Players take turns placing ships on a 10x10 grid and then attempt to sink each other's ships by selecting grid positions. The game provides a visual interface to track hits and misses.

Features:

-Two-player mode

-Ship placement with preview

-Turn-based gameplay

-Visual indicators for hits and misses

Installation:

-Prerequisites
-Ensure you have Python installed on your system. You will also need Pygame.

#Install Dependencies

-pip install pygame
-Run the Game
-python battleship.py

How to Play:

-Placing Ships
-Players take turns placing their ships.
-Click to place a ship, press R to rotate.
-After all ships are placed, the game proceeds to attack phase.
-Taking Turns
-Each player selects a grid position to attack.
-Hits are marked with a red circle, misses with an X.
-The game continues until all of one player's ships are sunk.

Known Bugs & Fixes:

#Bug 1: Ships Overlapping During Placement

Issue: Players can place ships on top of existing ships.
Fix: Implemented a check in can_place_ship() to ensure a ship does not overlap another ship.

#Bug 2: Grid Misalignment on Different Screen Sizes

Issue: The grid may not be centered correctly on different screen resolutions.
Fix: Adjusted GRID_OFFSET_X dynamically based on screen width.

#Bug 3: Clicking Outside the Grid Causes Errors

Issue: Clicking outside the valid grid range could cause an index error.
Fix: Added boundary checks before registering a move.

#Bug 4: Players Can See Each Other's Ships

Issue: Players could see ships when it wasn't their turn.
Fix: The game now uses view_board to ensure ships remain hidden from the opponent.

Future Improvements:

-AI mode for single-player gameplay.
-Enhanced UI/UX with animations.
-Different ship types with additional mechanics.
