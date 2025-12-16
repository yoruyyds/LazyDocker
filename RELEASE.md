# 🚀 LazyDocker Control - 发布说明

## 修复说明

### 问题：exe 运行后不自动打开浏览器

**原因：** Streamlit 在打包环境中的 `developmentMode` 配置冲突

**解决方案：**
1. 修改了 `run.py` 中的启动参数
2. 设置 `--server.headless=false` 允许自动打开浏览器
3. 设置 `--global.developmentMode=false` 禁用开发模式

### 重新打包步骤

#### 方法 1：使用批处理脚本（推荐）

```bash
build.bat
```

#### 方法 2：手动命令

```bash
# 清理旧文件
rmdir /s /q build
rmdir /s /q dist

# 重新打包
pyinstaller LazyDocker.spec
```

### 测试运行

打包完成后：

1. 确保 Docker Desktop 正在运行
2. 双击 `dist\LazyDocker.exe`
3. 浏览器应该会自动打开 `http://localhost:8501`
4. 如果没有自动打开，手动访问该地址

### 关键修改

**run.py 修改前：**
```python
sys.argv = [
    "streamlit",
    "run",
    app_path,
    "--server.headless=true",  # ❌ 阻止浏览器打开
    "--browser.gatherUsageStats=false",
    "--server.port=8501"  # ❌ 与 developmentMode 冲突
]
```

**run.py 修改后：**
```python
sys.argv = [
    "streamlit",
    "run",
    app_path,
    "--server.headless=false",  # ✅ 允许浏览器打开
    "--browser.gatherUsageStats=false",
    "--global.developmentMode=false"  # ✅ 禁用开发模式
]
```

## 常见问题

### Q1: 端口 8501 被占用怎么办？

**方法 1：** 关闭占用端口的程序
```bash
# 查找占用端口的进程
netstat -ano | findstr :8501

# 结束进程（替换 PID 为实际进程 ID）
taskkill /PID <PID> /F
```

**方法 2：** 修改 run.py 使用其他端口
```python
sys.argv = [
    "streamlit",
    "run",
    app_path,
    "--server.headless=false",
    "--browser.gatherUsageStats=false",
    "--global.developmentMode=false",
    "--server.port=8502"  # 改为其他端口
]
```

### Q2: 浏览器还是没有自动打开？

1. 检查默认浏览器设置
2. 手动访问 `http://localhost:8501`
3. 查看控制台输出的实际端口号

### Q3: 打包时间太长？

这是正常的，因为需要：
- 收集所有依赖（Streamlit、Docker SDK、NumPy 等）
- 打包成单个 exe 文件
- 通常需要 3-5 分钟

可以通过以下方式加速：
- 使用 SSD 硬盘
- 关闭杀毒软件的实时扫描
- 使用 `--onedir` 代替 `--onefile`（会生成文件夹）

### Q4: exe 文件太大（300+ MB）？

这是正常的，因为包含了：
- Python 运行时
- Streamlit 框架
- Docker SDK
- NumPy、Pandas 等科学计算库
- 所有依赖的 DLL 文件

如果需要减小体积：
1. 使用 `--onedir` 模式（文件夹形式）
2. 在 spec 文件的 `excludes` 中添加更多不需要的模块

## 版本信息

- **LazyDocker Control**: v1.0.0
- **Python**: 3.13.5
- **PyInstaller**: 6.17.0
- **Streamlit**: 1.28.0+
- **Docker SDK**: 6.1.0+

## 下一步

打包成功后，你可以：

1. **测试功能**：确保所有容器操作正常
2. **创建快捷方式**：将 exe 放到桌面或开始菜单
3. **分享给他人**：直接发送 exe 文件（需要对方安装 Docker）
4. **上传到 GitHub**：创建 Release 并上传 exe

## 发布到 GitHub

```bash
# 1. 创建 Release
git tag v1.0.0
git push origin v1.0.0

# 2. 在 GitHub 上创建 Release
# 3. 上传 dist\LazyDocker.exe
# 4. 添加发布说明
```

## 技术支持

如果遇到问题：
1. 查看控制台输出的错误信息
2. 检查 `build\LazyDocker\warn-LazyDocker.txt`
3. 在 GitHub Issues 中提问

---

**祝你使用愉快！** 🐳
