# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['..\\src\\main.py'],
    pathex=['..\src'],
    binaries=[],
    datas=[('..\\src\\ui\\themes\\main_theme.qss', 'src\\ui\\themes')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
#         splash,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GUI_client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='..\\src\\ui\\forms\\icons\\images\\program_icon.ico',
)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
#               splash.binaries,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='GUI_client'
)
