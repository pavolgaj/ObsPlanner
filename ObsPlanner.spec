# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/media/pavolg/Data/Palko/skola/python/ObsPlanner'],
             binaries=[],
             datas=[('ObsPlanner.png', '.'), ('data/bound_20.dat', 'data'), ('data/lines.txt', 'data'), ('data/stars.txt', 'data'), ('data/objects-messier.opd', 'data')],
             hiddenimports=['PIL', 'PIL._imagingtk', 'PIL._tkinter_finder'],
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
          [],
          exclude_binaries=True,
          name='ObsPlanner',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , version='version.txt', icon='ObsPlanner.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ObsPlanner')
