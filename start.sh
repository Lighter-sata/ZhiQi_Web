#!/bin/bash

# 芝栖养生平台 - 一键启动脚本 (Bash版本)
# 用于快速启动开发环境

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印横幅
print_banner() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                      🌿 芝栖养生平台 🌿                       ║"
    echo "║                 连接自然之力，引领品质生活                       ║"
    echo "║                                                              ║"
    echo "║  🔧 技术栈: Vue.js 3 + Flask + MySQL + Docker              ║"
    echo "║  📱 前端: http://localhost:8080                             ║"
    echo "║  🔗 后端API: http://localhost:5000                          ║"
    echo "║  🗄️ 数据库: localhost:3306                                  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 打印状态信息
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 检查系统要求
check_requirements() {
    echo "🔍 检查系统要求..."

    # 检查Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_status "Python $PYTHON_VERSION"
    else
        print_error "Python 3 未安装"
        echo "请访问 https://www.python.org 下载安装 Python 3.8+"
        exit 1
    fi

    # 检查Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_status "Node.js $NODE_VERSION"
    else
        print_error "Node.js 未安装"
        echo "请访问 https://nodejs.org 下载安装 Node.js 16+"
        exit 1
    fi

    # 检查npm
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        print_status "npm $NPM_VERSION"
    else
        print_error "npm 未安装"
        exit 1
    fi

    # 检查Docker (可选)
    if command_exists docker; then
        DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
        print_status "Docker $DOCKER_VERSION"
        USE_DOCKER=true
    else
        print_warning "Docker 未安装，将使用本地开发模式"
        USE_DOCKER=false
    fi

    # 检查docker-compose (如果有Docker)
    if [ "$USE_DOCKER" = true ] && command_exists docker-compose; then
        DC_VERSION=$(docker-compose --version | awk '{print $3}')
        print_status "Docker Compose $DC_VERSION"
    fi
}

# 检查项目文件
check_project_files() {
    echo ""
    echo "🔍 检查项目文件..."

    local required_files=(
        "backend/app.py"
        "backend/requirements.txt"
        "backend/schema.sql"
        "frontend/package.json"
        "frontend/src/main.js"
        "frontend/src/App.vue"
        "docker-compose.yml"
    )

    local missing_files=()

    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done

    if [ ${#missing_files[@]} -ne 0 ]; then
        print_error "缺少以下文件:"
        for file in "${missing_files[@]}"; do
            echo "   - $file"
        done
        exit 1
    fi

    print_status "项目文件完整"
}

# 设置后端环境
setup_backend() {
    echo ""
    echo "🐍 设置后端环境..."

    cd backend

    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo "📦 创建Python虚拟环境..."
        python3 -m venv venv
    fi

    # 激活虚拟环境并安装依赖
    echo "📦 安装Python依赖..."
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        ./venv/Scripts/pip install -r requirements.txt
    else
        # macOS/Linux
        ./venv/bin/pip install -r requirements.txt
    fi

    print_status "后端依赖安装完成"
    cd ..
}

# 设置前端环境
setup_frontend() {
    echo ""
    echo "🎨 设置前端环境..."

    cd frontend

    # 检查node_modules
    if [ ! -d "node_modules" ]; then
        echo "📦 安装Node.js依赖..."
        npm install
    else
        print_status "前端依赖已存在"
    fi

    print_status "前端环境准备完成"
    cd ..
}

# 启动服务
start_services() {
    echo ""
    echo "🚀 启动服务..."

    if [ "$USE_DOCKER" = true ]; then
        start_docker_services
    else
        start_local_services
    fi
}

# 使用Docker启动服务
start_docker_services() {
    echo "🐳 使用Docker模式启动..."

    # 启动服务
    docker-compose up -d

    # 等待服务启动
    echo "⏳ 等待服务启动..."
    sleep 15

    # 检查服务状态
    if docker-compose ps | grep -q "Up"; then
        print_status "Docker服务启动成功"
    else
        print_error "Docker服务启动失败"
        docker-compose logs
        exit 1
    fi
}

# 使用本地开发模式启动服务
start_local_services() {
    echo "💻 使用本地开发模式启动..."

    # 检查MySQL服务
    echo "🗄️ 请确保MySQL服务正在运行..."
    echo "   MySQL默认端口: 3306"
    echo "   数据库: wellness_platform_db"
    echo "   用户: root"
    echo ""

    # 创建后端启动脚本
    cat > backend/start_local.py << 'EOF'
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置环境变量
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('DATABASE_URL', 'mysql+mysqlconnector://root:password@localhost/wellness_platform_db')
os.environ.setdefault('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')

# 启动应用
from backend.app import app

if __name__ == '__main__':
    print("🐍 启动Flask后端服务...")
    print("📡 服务地址: http://localhost:5000")
    print("📚 API文档: http://localhost:5000 (Swagger UI)")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF

    # 启动后端服务 (后台运行)
    echo "🐍 启动后端服务..."
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        start python backend/start_local.py
    else
        # macOS/Linux
        python3 backend/start_local.py &
        BACKEND_PID=$!
        echo $BACKEND_PID > .backend_pid
    fi

    sleep 3

    # 启动前端服务 (后台运行)
    echo "🎨 启动前端服务..."
    cd frontend
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        start npm run serve
    else
        # macOS/Linux
        npm run serve &
        FRONTEND_PID=$!
        echo $FRONTEND_PID > ../.frontend_pid
    fi
    cd ..

    sleep 5
    print_status "本地服务启动完成"
}

# 打开浏览器
open_browser() {
    echo ""
    echo "🌐 打开浏览器..."

    sleep 3

    # 尝试打开浏览器
    if command_exists xdg-open; then
        # Linux
        xdg-open http://localhost:8080 2>/dev/null &
    elif command_exists open; then
        # macOS
        open http://localhost:8080
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        start http://localhost:8080
    else
        print_warning "无法自动打开浏览器"
    fi

    print_status "浏览器已打开，访问: http://localhost:8080"
}

# 清理函数
cleanup() {
    echo ""
    echo "🧹 清理临时文件..."

    # 停止后台进程
    if [ -f .backend_pid ]; then
        kill $(cat .backend_pid) 2>/dev/null || true
        rm .backend_pid
    fi

    if [ -f .frontend_pid ]; then
        kill $(cat .frontend_pid) 2>/dev/null || true
        rm .frontend_pid
    fi

    # 删除临时文件
    rm -f backend/start_local.py

    print_status "清理完成"
}

# 信号处理
trap cleanup SIGINT SIGTERM

# 主函数
main() {
    # 打印横幅
    print_banner

    # 检查要求
    check_requirements

    # 检查项目文件
    check_project_files

    # 设置环境
    setup_backend
    setup_frontend

    # 启动服务
    start_services

    # 打开浏览器
    open_browser

    # 打印成功信息
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                     🎉 启动成功！🎉                          ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  📱 前端应用: http://localhost:8080                         ║"
    echo "║  🔗 后端API:  http://localhost:5000                         ║"
    echo "║  📚 API文档:  http://localhost:5000 (Swagger UI)           ║"
    echo "║  🗄️ 数据库:   localhost:3306 (MySQL)                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "按 Ctrl+C 停止所有服务"
    echo ""

    # 保持运行
    while true; do
        sleep 1
    done
}

# 运行主函数
main "$@"
