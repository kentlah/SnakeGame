# SnakeGame

A Snake game implemented in Python using Pygame.

This project demonstrates:

-   Object-oriented design
-   Game loop architecture
-   Event-driven input handling
-   Collision detection
-   Configurable gameplay options
-   Debug overlay implementation

------------------------------------------------------------------------

## Requirements

-   Python 3.x
-   pygame

Install dependency:

    pip install pygame

------------------------------------------------------------------------

## How to Run

From the project directory:

    python Ass4SnakeFinal.py.py

The game launches into the main menu.

------------------------------------------------------------------------

## Game Overview

-   Window size: 640 x 480
-   Grid size: 10 x 10 pixel blocks
-   Frame rate controlled dynamically by snake speed
-   Initial snake speed: 10
-   Maximum snake speed: 30
-   Score increases by 10 per worm eaten

------------------------------------------------------------------------

## Controls

Movement: - Arrow Keys or WASD → Move snake

Menu: - Up / W → Move selection up - Down / S → Move selection down -
Enter → Toggle option / Start game - Escape → Quit from menu

In-Game: - P → Pause / Unpause - Escape → Return to main menu (resets
game) - F5 → Toggle debug mode

Game Over Screen: - Mouse Click → Return to main menu - Escape → Quit

------------------------------------------------------------------------

## Gameplay Mechanics

### Snake

-   Moves in 10-pixel increments
-   Cannot reverse direction directly
-   Grows when eating a worm
-   Collision detection includes:
    -   Self-collision
    -   Border collision (if borders enabled)
-   Wraparound behavior when borders are disabled

### Worm

-   Spawns at random grid-aligned positions
-   Respawns when eaten
-   Tracks spawn time for timer logic

------------------------------------------------------------------------

## Menu Options

The following options can be toggled from the main menu:

-   Borders
    -   On: Collision with screen edges ends the game\
    -   Off: Snake wraps around screen edges
-   Score
    -   Displays score in top-left corner
-   Worm Timer
    -   Worm despawns after 10 seconds\
    -   If snake length \> 3: last segment is removed\
    -   If snake length ≤ 3: game ends
-   Increase Speed
    -   Snake speed increases by 1 each time a worm is eaten\
    -   Maximum speed: 30

------------------------------------------------------------------------

## Debug Mode (F5)

Displays real-time debugging information:

-   Worm position
-   Snake head position
-   Current speed
-   Worm timer countdown
-   Current snake length

------------------------------------------------------------------------

## Architecture Overview

### Classes

Snake - Handles movement, direction changes, growth, and collision
detection - Maintains body positions as a list - Supports speed
increases

Worm - Handles spawning logic - Tracks spawn time for timer feature

Game - Manages overall game state - Handles menu system - Controls game
loop - Manages pause functionality - Draws UI elements and debug overlay

------------------------------------------------------------------------

## Technical Concepts Demonstrated

-   Game loop design
-   State management
-   Modular class structure
-   Collision detection logic
-   Input handling with pygame
-   Conditional gameplay features
-   Real-time debugging overlay

------------------------------------------------------------------------

## Potential Improvements

-   Sound effects
-   High score persistence
-   Improved UI styling
-   Adjustable difficulty levels
-   Configurable grid size
-   Refactoring menu into separate component


Using the escape key from the main menu will close the game entirely.

Using the 'P' button while in game will pause the game. 




