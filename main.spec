# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py', 'Game.py', 'Control.py', 'Game_Over.py', 'Menu.py', 'Piece.py', 'Player.py', 'States.py', 'Globals.py', 'Text.py', 'Tile.py'],
#a = Analysis(['main.py'],
             pathex=['C:\\Users\\Spencer\\Documents\\Tetrisn-t'],
             binaries=[],
             datas=[('resources/backgroundblock.bmp', '.'),
                    ('resources/IOTblock.bmp',        '.'),
                    ('resources/iconsmall.bmp',       '.'),
                    ('resources/JSblock.bmp',         '.'),
                    ('resources/LZblock.bmp',         '.'),
                    ('resources/munro-small.ttf',     '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
