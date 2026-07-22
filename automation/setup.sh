#!/bin/bash
# Streamlit Cloud 部署设置脚本
# 此脚本在 Streamlit Cloud 部署时自动运行
# 参考: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/app-dependencies

set -e  # 出错时停止执行

echo "=== Running setup.sh for Streamlit Cloud ==="

# 安装 lxml 所需的系统依赖（某些环境中需要）
# apt-get update -qq && apt-get install -y -qq libxml2-dev libxslt-dev 2>/dev/null || true

# 创建 .streamlit 目录（如果不存在）
mkdir -p ~/.streamlit/

# 如果用户没有上传 .streamlit/config.toml，可以在此生成默认配置
# 但推荐直接将 .streamlit/config.toml 提交到仓库
if [ ! -f ~/.streamlit/config.toml ]; then
    cat > ~/.streamlit/config.toml << 'CONFIG'
[theme]
primaryColor = "#4B3FE3"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F9FAFB"
textColor = "#111827"
font = "sans serif"
CONFIG
    echo "Created default .streamlit/config.toml"
fi

echo "=== setup.sh completed ==="
