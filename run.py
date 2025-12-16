"""
LazyDocker Control - 启动脚本
用于 PyInstaller 打包的入口文件
"""

import sys
import os
from streamlit.web import cli as stcli


def main():
    """
    启动 Streamlit 应用
    """
    # 获取 app.py 的路径
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe 运行
        application_path = sys._MEIPASS
    else:
        # 如果是直接运行 Python 脚本
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # app.py 的完整路径
    app_path = os.path.join(application_path, 'app.py')
    
    # 模拟命令行参数，启动 Streamlit
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.headless=false",  # 改为 false 以自动打开浏览器
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false"
    ]
    
    # 启动 Streamlit
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
