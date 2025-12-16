# 🔨 LazyDocker Control - 打包指南

本文档说明如何将 LazyDocker Control 打包成 Windows exe 可执行文件。

## 📋 前置要求

- Python 3.8 或更高版本
- 已安装项目依赖（`pip install -r requirements.txt`）
- Windows 操作系统

## 🚀 打包步骤

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 方法一：使用 spec 文件打包（推荐）

这是最稳定的方法，所有配置都在 `LazyDocker.spec` 文件中。

```bash
pyinstaller LazyDocker.spec
```

打包完成后，exe 文件位于 `dist/LazyDocker.exe`

### 3. 方法二：使用命令行打包

如果你想自定义打包参数，可以使用以下命令：

```bash
pyinstaller --onefile --name LazyDocker --add-data "app.py;." --hidden-import streamlit.web.cli --hidden-import streamlit.runtime.scriptrunner.magic_funcs --hidden-import docker --hidden-import docker.errors --collect-all streamlit --console run.py
```

**参数说明：**
- `--onefile`: 打包成单个 exe 文件
- `--name LazyDocker`: 输出文件名
- `--add-data "app.py;."`: 将 app.py 打包进去（Windows 使用分号）
- `--hidden-import`: 添加隐藏导入的模块
- `--collect-all streamlit`: 收集 Streamlit 的所有文件
- `--console`: 保留控制台窗口（可以看到 Streamlit 日志）

**如果想隐藏控制台窗口（不推荐，会看不到日志）：**
```bash
pyinstaller --onefile --noconsole --name LazyDocker --add-data "app.py;." --hidden-import streamlit.web.cli --hidden-import streamlit.runtime.scriptrunner.magic_funcs --hidden-import docker --hidden-import docker.errors --collect-all streamlit run.py
```

## 📦 打包后的文件

打包完成后，你会看到以下目录结构：

```
.
├── build/              # 临时构建文件（可删除）
├── dist/               # 输出目录
│   └── LazyDocker.exe  # 最终的可执行文件
├── LazyDocker.spec     # PyInstaller 配置文件
└── ...
```

## ✅ 测试打包结果

1. 确保 Docker Desktop 正在运行
2. 双击 `dist/LazyDocker.exe`
3. 浏览器会自动打开 `http://localhost:8501`
4. 如果没有自动打开，手动访问该地址

## ⚠️ 常见问题

### 问题 1: 提示找不到 streamlit 模块

**解决方案：** 使用 spec 文件打包，或确保添加了所有 hidden-import

### 问题 2: exe 文件很大（超过 100MB）

**原因：** Streamlit 和 Docker SDK 包含了很多依赖
**解决方案：** 这是正常的，单文件打包会包含所有依赖

### 问题 3: 无法连接 Docker

**解决方案：** 
- 确保 Docker Desktop 正在运行
- 确保 Docker socket 可访问
- 以管理员身份运行 exe

### 问题 4: 打包后运行报错

**解决方案：** 
- 保留 `--console` 参数查看错误日志
- 检查是否所有依赖都已安装
- 尝试使用 spec 文件打包

## 🎯 优化建议

### 添加图标

1. 准备一个 `.ico` 图标文件（例如 `icon.ico`）
2. 在 spec 文件中修改：
   ```python
   icon='icon.ico'
   ```
3. 或在命令行中添加：
   ```bash
   --icon=icon.ico
   ```

### 减小文件大小

如果需要减小 exe 文件大小，可以：
1. 使用 `--onedir` 代替 `--onefile`（会生成一个文件夹）
2. 排除不需要的模块：`--exclude-module matplotlib`

## 📤 发布

打包完成后，你可以：
1. 直接分享 `dist/LazyDocker.exe` 文件
2. 创建安装程序（使用 Inno Setup 或 NSIS）
3. 上传到 GitHub Releases

## 🔄 重新打包

如果修改了代码，重新打包：

```bash
# 清理旧文件
rmdir /s /q build dist
del LazyDocker.spec

# 重新打包
pyinstaller LazyDocker.spec
```

## 📝 注意事项

1. **首次运行较慢**：exe 首次运行时会解压临时文件，需要几秒钟
2. **杀毒软件**：某些杀毒软件可能误报，需要添加信任
3. **Docker 依赖**：用户电脑上必须安装 Docker Desktop
4. **网络端口**：确保 8501 端口未被占用

## 🆘 获取帮助

如果遇到问题：
1. 查看控制台输出的错误信息
2. 检查 PyInstaller 的日志文件
3. 在 GitHub Issues 中提问
