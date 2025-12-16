# 🐳 LazyDocker Control

一个基于 Streamlit 构建的轻量级 Docker 容器管理面板，提供简洁直观的 Web 界面来管理本地 Docker 容器。

## ✨ 功能特性

- 🔍 **实时监控**: 自动扫描并显示所有 Docker 容器（运行中和已停止）
- 🎨 **卡片式设计**: 每个容器独立卡片展示，界面清晰美观
- 🚀 **一键操作**: 快速启动/停止容器
- 🌐 **端口跳转**: 自动检测端口映射，一键打开容器服务
- 📊 **统计信息**: 实时显示容器运行状态统计
- ⚡ **即时刷新**: 操作后自动刷新，状态实时更新

## 🛠️ 技术栈

- **Streamlit**: Web 界面框架
- **Docker SDK for Python**: Docker API 交互

## 📦 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/lazydocker-control.git
cd lazydocker-control
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 🚀 使用方法

1. 确保 Docker Desktop 正在运行

2. 启动应用：
```bash
streamlit run app.py
```

3. 浏览器会自动打开 `http://localhost:8501`

## 📸 功能说明

### 运行中的容器
- 显示 🟢 绿色状态指示
- 展示容器名称和镜像信息
- 提供"打开"按钮（如果有端口映射）
- 提供"停止"按钮

### 已停止的容器
- 显示 🔴 红色状态指示
- 展示容器名称和镜像信息
- 提供"启动容器"按钮

### 侧边栏
- 刷新状态按钮
- 容器统计信息（运行中/已停止/总计）

## ⚠️ 注意事项

- 需要 Docker Desktop 或 Docker Engine 正在运行
- 确保当前用户有权限访问 Docker socket
- Windows 用户需要确保 Docker Desktop 已启动

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 👨‍💻 作者

kuuruv

