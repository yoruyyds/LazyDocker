"""
PyInstaller Hook for Streamlit
解决 Streamlit 打包时的 metadata 和隐藏导入问题
"""

from PyInstaller.utils.hooks import copy_metadata, collect_data_files, collect_submodules

# 收集 Streamlit 的 metadata
datas = copy_metadata('streamlit')

# 收集 Streamlit 的数据文件
datas += collect_data_files('streamlit')

# 收集所有 Streamlit 子模块
hiddenimports = collect_submodules('streamlit')

# 添加其他必要的隐藏导入
hiddenimports += [
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'altair',
    'validators',
    'watchdog',
    'tornado',
    'click',
]
