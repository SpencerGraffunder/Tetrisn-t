# Description

Tetrisn-t is a Tetris-like game (that is not Tetris) where any number of players can play (eventually that update will come).  
Network is setup by the user via port forwarding (think Minecraft servers), but local play is supported.  
Currently only keyboard controls; controller support planned for future update.

# Install / Run

Tetrisn-t is programmed in Python 3.

## Windows

Either open the `.exe` file if there is one, or to run with Python do the following:

1. Download and install Python 3 (latest) via the official Python website https://www.python.org/downloads/windows/  
2. Open a terminal (press the Windows key then type `terminal` and hit enter) and type `pip install pygame` (then hit enter)  
3. To run the game, open a file manager to Tetrisn-t\ and run `main.py` with Python (should automatically be set to the default program)

After all three steps are completed successfully, running the game again requires only step 3.  
Suggestion: Select `main.py` in a file manager, right click, and create a shortcut to open the program from somewhere else. It is unsafe to move the game files around, as the file paths are hard-coded.

## Linux

Install Python 3, then

```
pip3 install pygame
```

(currently not necessary, but maybe someday: `sudo apt-get install python-pil`)

To run the game:

```
python3 main.py
```

## Create .exe

```
pip install pyinstaller
```

```
pyinstaller main.spec
```

# Game Mechanics

## Frame Data

Almost everything in Tetrisn-t regarding frame data works much the same way as the 1989 version of Tetris does, with a few things difficult to perfect, but it should get closer over time. See https://tetris.wiki/Tetris_(NES,_Nintendo)

## Levels / Score

Same as "Frame Data"

## RNG

The only RNG aspect of the game is the piece type. It is the same as the 1989 NES Tetris, and in multiplayer it is still the same but with each person having their own independent RNG

## Multiplayer

Inspired by Tetris Tengen, but with the idea that any number of players can play (and the pieces don't freeze in mid-air when each player holds towards one another)

## Special

Currently, there is an easter egg where if one player tucks a piece under an overhang and another player clears a few lines immediately after, the board will move down and possibly cause a game over. This is because of the game over mechanics of the 1989 version of Tetris. Eventually, this is planned to be fixed by causing the tucked, active piece to be "forced down with" the board as the lines move down, but only when there are piece tiles above the active piece

DAS doesn't work when there is no active piece for a given player (to be fixed)

# Develop

Currently we are not very open to allow new developers onto the Tetrisn-t team, but once we have a better functioning game we will consider allowing others to improve functionality or add quality of life improvements

See README.dev for the documentation
