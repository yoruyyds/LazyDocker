"""
LazyDocker Control - Docker 容器管理面板
基于 Streamlit 构建的轻量级 Docker 容器管理工具
"""

import streamlit as st
import docker
from docker.errors import DockerException
from collections import defaultdict


# 页面配置
st.set_page_config(
    page_title="LazyDocker Control",
    page_icon="🐳",
    layout="wide"
)


# 容器分类规则映射
CATEGORY_MAP = {
    "🎨 AI 绘画": ["comfy", "stable", "sd", "diffusion", "webui"],
    "🤖 大模型/聊天": ["gpt", "ollama", "deepseek", "llama", "chatgpt", "openai"],
    "🗄️ 数据库": ["mysql", "redis", "postgres", "mongodb", "mariadb", "elasticsearch"],
    "⬇️ 下载工具": ["qbittorrent", "transmission", "aria2", "download"],
    "🌐 Web 服务": ["nginx", "apache", "caddy", "traefik"],
    "📊 监控工具": ["grafana", "prometheus", "portainer", "netdata"],
}

# 默认分类
DEFAULT_CATEGORY = "📦 其他应用"

# 常用 Web 端口优先级列表
PREFERRED_WEB_PORTS = [80, 8080, 8188, 3000, 5000, 7860, 443, 8000, 8888, 9000]

# 数据库端口黑名单（不应通过浏览器访问）
DATABASE_PORTS = [3306, 5432, 6379, 27017, 1433, 5984, 9042, 7000, 7001]


def connect_docker():
    """
    连接到本地 Docker 守护进程
    
    Returns:
        docker.DockerClient: Docker 客户端实例，连接失败返回 None
    """
    try:
        client = docker.from_env()
        # 测试连接
        client.ping()
        return client
    except DockerException as e:
        st.error(f"❌ 无法连接到 Docker！请确保 Docker Desktop 正在运行。\n\n错误信息: {str(e)}")
        return None


def categorize_container(container_name):
    """
    根据容器名称自动分类
    
    Args:
        container_name: 容器名称
        
    Returns:
        str: 分类名称
    """
    container_name_lower = container_name.lower()
    
    for category, keywords in CATEGORY_MAP.items():
        for keyword in keywords:
            if keyword in container_name_lower:
                return category
    
    return DEFAULT_CATEGORY


def get_all_ports(container):
    """
    获取容器所有映射到宿主机的端口
    
    Args:
        container: Docker 容器对象
        
    Returns:
        list: 端口列表，例如 [8080, 3000]，如果没有端口映射则返回空列表
    """
    # 检查容器是否有端口映射
    ports_config = container.attrs.get('NetworkSettings', {}).get('Ports', {})
    
    if not ports_config:
        return []
    
    # 收集所有映射到宿主机的端口
    available_ports = []
    for container_port, host_bindings in ports_config.items():
        if host_bindings:  # 确保有宿主机绑定
            for binding in host_bindings:
                if binding and 'HostPort' in binding:
                    try:
                        port = int(binding['HostPort'])
                        available_ports.append(port)
                    except (ValueError, TypeError):
                        continue
    
    return available_ports


def get_web_ports(ports):
    """
    从端口列表中过滤出 Web 端口（排除数据库端口）
    
    Args:
        ports: 端口列表
        
    Returns:
        list: Web 端口列表，按优先级排序
    """
    # 过滤掉数据库端口
    web_ports = [p for p in ports if p not in DATABASE_PORTS]
    
    if not web_ports:
        return []
    
    # 按优先级排序：优先端口在前，其他端口在后
    priority_ports = [p for p in PREFERRED_WEB_PORTS if p in web_ports]
    other_ports = [p for p in web_ports if p not in PREFERRED_WEB_PORTS]
    
    return priority_ports + other_ports


def has_only_database_ports(ports):
    """
    检查是否只有数据库端口
    
    Args:
        ports: 端口列表
        
    Returns:
        bool: 如果所有端口都是数据库端口返回 True
    """
    if not ports:
        return False
    return all(p in DATABASE_PORTS for p in ports)


def render_container_card(container):
    """
    渲染单个容器的卡片界面
    
    Args:
        container: Docker 容器对象
    """
    # 创建卡片容器
    with st.container(border=True):
        # 获取容器基本信息
        container_name = container.name
        container_status = container.status
        image_name = container.image.tags[0] if container.image.tags else container.image.short_id
        
        # 根据状态显示不同的 UI
        if container_status == 'running':
            # 情况 A: 容器正在运行
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### 🟢 {container_name}")
                st.caption(f"📦 镜像: `{image_name}`")
                st.caption(f"✅ 状态: Running")
            
            with col2:
                # 获取所有端口
                all_ports = get_all_ports(container)
                web_ports = get_web_ports(all_ports)
                
                if web_ports:
                    # 有 Web 端口，显示打开按钮
                    if len(web_ports) == 1:
                        # 单个端口，显示一个按钮
                        st.link_button(
                            f"🔗 打开 [{web_ports[0]}]",
                            f"http://localhost:{web_ports[0]}",
                            use_container_width=True
                        )
                    else:
                        # 多个端口，并排显示多个按钮
                        port_cols = st.columns(len(web_ports))
                        for idx, port in enumerate(web_ports):
                            with port_cols[idx]:
                                st.link_button(
                                    f"🔗 {port}",
                                    f"http://localhost:{port}",
                                    use_container_width=True
                                )
                elif has_only_database_ports(all_ports):
                    # 只有数据库端口
                    st.info("💾 数据库服务")
                    st.caption("(不可通过浏览器访问)")
                elif all_ports:
                    # 有端口但都被过滤了（内部端口）
                    st.warning("⛔ 仅内部端口")
                    st.caption("(No Public Mapping)")
                else:
                    # 完全没有端口映射
                    st.warning("⛔ 未映射端口")
                    st.caption("(Internal Only)")
                
                # 停止按钮
                if st.button(f"⏹️ 停止", key=f"stop_{container.id}", use_container_width=True):
                    try:
                        container.stop()
                        st.success(f"✅ 容器 {container_name} 已停止")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 停止失败: {str(e)}")
        
        elif container_status == 'restarting':
            # 情况 C: 容器正在重启
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### 🟡 {container_name}")
                st.caption(f"📦 镜像: `{image_name}`")
                st.caption(f"⚠️ 状态: Restarting...")
                st.caption("💡 提示: 容器可能遇到问题，请检查日志")
            
            with col2:
                # 重启中的容器，提供停止选项
                if st.button(f"⏹️ 强制停止", key=f"stop_{container.id}", use_container_width=True):
                    try:
                        container.stop()
                        st.success(f"✅ 容器 {container_name} 已停止")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 停止失败: {str(e)}")
        
        else:
            # 情况 D: 容器已停止或其他状态
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### 🔴 {container_name}")
                st.caption(f"📦 镜像: `{image_name}`")
                st.caption(f"⏸️ 状态: {container_status.capitalize()}")
            
            with col2:
                # 启动按钮
                if st.button(f"🚀 启动容器", key=f"start_{container.id}", use_container_width=True):
                    try:
                        container.start()
                        st.success(f"✅ 容器 {container_name} 已启动")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 启动失败: {str(e)}")


def main():
    """
    主函数 - 应用入口
    """
    # 页面标题
    st.title("🐳 LazyDocker Control")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 控制面板")
        if st.button("🔄 刷新状态", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 统计信息")
    
    # 连接 Docker
    client = connect_docker()
    
    if client is None:
        st.stop()
    
    # 获取所有容器
    try:
        containers = client.containers.list(all=True)
        
        if not containers:
            st.info("ℹ️ 当前没有任何容器")
            return
        
        # 统计信息
        running_count = sum(1 for c in containers if c.status == 'running')
        stopped_count = len(containers) - running_count
        
        with st.sidebar:
            st.metric("运行中", running_count)
            st.metric("已停止", stopped_count)
            st.metric("总计", len(containers))
        
        # 按分类组织容器
        categorized_containers = defaultdict(list)
        for container in containers:
            category = categorize_container(container.name)
            categorized_containers[category].append(container)
        
        # 显示容器列表
        st.subheader(f"📦 容器列表 ({len(containers)} 个)")
        
        # 按分类显示容器
        # 先显示有容器的预定义分类
        for category in CATEGORY_MAP.keys():
            if category in categorized_containers:
                with st.expander(f"**{category}** ({len(categorized_containers[category])} 个)", expanded=True):
                    for container in categorized_containers[category]:
                        render_container_card(container)
        
        # 最后显示"其他应用"分类
        if DEFAULT_CATEGORY in categorized_containers:
            with st.expander(f"**{DEFAULT_CATEGORY}** ({len(categorized_containers[DEFAULT_CATEGORY])} 个)", expanded=True):
                for container in categorized_containers[DEFAULT_CATEGORY]:
                    render_container_card(container)
    
    except Exception as e:
        st.error(f"❌ 获取容器列表失败: {str(e)}")


if __name__ == "__main__":
    main()
