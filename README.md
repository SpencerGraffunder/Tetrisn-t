# Description

Tetrisn-t is a Tetris-like game (that is not Tetris) where any number of players can play (eventually that update will come).  
Network is setup by the user via port forwarding (think Minecraft servers), but local play is supported.  
Currently only keyboard controls; controller support planned for future update.

# Install / Run

Tetrisn-t is programmed in Python 3.

## Windows

Either open the `.exe` file, or to run with Python...

1. Download and install Python 3 (latest) via the official Python website https://www.python.org/downloads/windows/  
2. Open a terminal (press the Windows key then type `terminal` and hit enter) and type `pip install pygame` (then hit enter)  
3. All setup is done. To run the game, open a file manager and run `main.py` with Python (should automatically be set to the default program)

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
pyinstaller main.spec
```

# Develop

Currently we are not very open to allow new developers onto the Tetrisn-t team, but once we have a better functioning game we will consider allowing others to improve functionality or add quality of life improvements.

See README.developer for the documentation.
