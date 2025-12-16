# -*- mode: python ; coding: utf-8 -*-
"""
LazyDocker Control - PyInstaller 配置文件
用于打包 Streamlit 应用为 Windows exe
"""

import sys
from PyInstaller.utils.hooks import copy_metadata, collect_data_files

block_cipher = None

# 收集 Streamlit 和 Docker 的 metadata
datas = []
datas += copy_metadata('streamlit')
datas += copy_metadata('docker')
datas += copy_metadata('altair')
datas += copy_metadata('validators')

# 收集 Streamlit 的静态文件
datas += collect_data_files('streamlit')

# 添加 app.py 作为数据文件
datas += [('app.py', '.')]

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'altair',
        'validators',
        'watchdog',
        'tornado',
        'click',
        'docker',
        'docker.errors',
    ],
    hookspath=['./'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'tkinter',
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'pytest',
        'black',
        'yapf',
        'sklearn',
        'skimage',
        'astropy',
        'dask',
        'distributed',
        'numba',
        'llvmlite',
        'tensorflow',
        'torch',
        'keras',
        'statsmodels',
        'patsy',
        'bokeh',
        'holoviews',
        'panel',
        'intake',
        'xarray',
        'h5py',
        'tables',
        'openpyxl',
        'xlrd',
        'xlwt',
        'nbconvert',
        'nbformat',
        'mistune',
        'docutils',
        'lxml',
        'imageio',
        'pywt',
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LazyDocker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 保留控制台窗口以查看 Streamlit 日志
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有 .ico 图标文件，可以在这里指定
)
