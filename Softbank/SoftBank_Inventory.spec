# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['SoftBank_Inventory.py'],
    pathex=[],
    binaries=[],
    datas=[('SoftBank_StockCalculate.py', '.'), ('SoftBank_ExceltoDB_Select.py', '.'), ('SoftBank_SummaryTable_Export.py', '.'), ('softbankapp.py', '.'), ('D:/DeltaBox/OneDrive - Delta Electronics, Inc/deltaproject/DEJbackup/Softbank/Pic/delta2.jpg', 'Pic/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SoftBank_Inventory',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
