#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
芝栖养生平台 - 一键启动脚本
用于快速启动开发环境
"""

import os
import sys
import time
import subprocess
import webbrowser
import platform
from pathlib import Path

class WellnessPlatformLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.is_windows = platform.system() == "Windows"

    def print_banner(self):
        """打印启动横幅"""
        banner = """
        ╔══════════════════════════════════════════════════════════════╗
        ║                      🌿 芝栖养生平台 🌿                       ║
        ║                 连接自然之力，引领品质生活                       ║
        ║                                                              ║
        ║  🔧 技术栈: Vue.js 3 + Flask + MySQL + Docker              ║
        ║  📱 前端: http://localhost:8080                             ║
        ║  🔗 后端API: http://localhost:5000                          ║
        ║  🗄️ 数据库: localhost:3306                                  ║
        ╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def check_requirements(self):
        """检查系统要求"""
        print("🔍 检查系统要求...")

        # 检查Python版本
        python_version = sys.version_info
        if python_version < (3, 8):
            print("❌ Python 3.8+ 版本要求，当前版本:", sys.version)
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")

        # 检查Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js {result.stdout.strip()}")
            else:
                print("❌ Node.js 未安装")
                return False
        except FileNotFoundError:
            print("❌ Node.js 未安装，请访问 https://nodejs.org 下载安装")
            return False

        # 检查npm
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm {result.stdout.strip()}")
            else:
                print("❌ npm 未安装")
                return False
        except FileNotFoundError:
            print("❌ npm 未安装")
            return False

        # 检查Docker
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Docker {result.stdout.strip()}")
                return True
            else:
                print("⚠️  Docker 未安装，将使用本地开发模式")
                return True
        except FileNotFoundError:
            print("⚠️  Docker 未安装，将使用本地开发模式")
            return True

    def check_project_files(self):
        """检查项目文件完整性"""
        print("\n🔍 检查项目文件...")

        required_files = [
            "backend/app.py",
            "backend/requirements.txt",
            "backend/schema.sql",
            "frontend/package.json",
            "frontend/src/main.js",
            "frontend/src/App.vue",
            "docker-compose.yml"
        ]

        missing_files = []
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                missing_files.append(file_path)

        if missing_files:
            print("❌ 缺少以下文件:")
            for file in missing_files:
                print(f"   - {file}")
            return False

        print("✅ 项目文件完整")
        return True

    def setup_backend(self):
        """设置后端环境"""
        print("\n🐍 设置后端环境...")

        if not self.backend_dir.exists():
            print("❌ 后端目录不存在")
            return False

        # 检查虚拟环境
        venv_path = self.backend_dir / "venv"
        if not venv_path.exists():
            print("📦 创建Python虚拟环境...")
            try:
                subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            except subprocess.CalledProcessError:
                print("❌ 创建虚拟环境失败")
                return False

        # 激活虚拟环境并安装依赖
        print("📦 安装Python依赖...")
        pip_cmd = str(venv_path / "bin" / "pip") if not self.is_windows else str(venv_path / "Scripts" / "pip")

        try:
            subprocess.run([pip_cmd, "install", "-r", str(self.backend_dir / "requirements.txt")], check=True)
            print("✅ 后端依赖安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ 后端依赖安装失败")
            return False

    def setup_frontend(self):
        """设置前端环境"""
        print("\n🎨 设置前端环境...")

        if not self.frontend_dir.exists():
            print("❌ 前端目录不存在")
            return False

        # 检查node_modules
        node_modules = self.frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 安装Node.js依赖...")
            try:
                subprocess.run(["npm", "install"], cwd=self.frontend_dir, check=True)
                print("✅ 前端依赖安装完成")
            except subprocess.CalledProcessError:
                print("❌ 前端依赖安装失败")
                return False
        else:
            print("✅ 前端依赖已存在")

        return True

    def start_services(self):
        """启动所有服务"""
        print("\n🚀 启动服务...")

        # 检查是否使用Docker
        use_docker = False
        try:
            subprocess.run(["docker", "info"], capture_output=True, check=True)
            use_docker = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            use_docker = False

        if use_docker:
            print("🐳 使用Docker模式启动...")
            return self.start_docker_services()
        else:
            print("💻 使用本地开发模式启动...")
            return self.start_local_services()

    def start_docker_services(self):
        """使用Docker启动服务"""
        try:
            print("🐳 启动Docker服务...")
            subprocess.run(["docker-compose", "up", "-d"], check=True)

            # 等待服务启动
            print("⏳ 等待服务启动...")
            time.sleep(10)

            # 检查服务状态
            result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
            if "Up" in result.stdout:
                print("✅ Docker服务启动成功")
                return True
            else:
                print("❌ Docker服务启动失败")
                print("服务状态:")
                print(result.stdout)
                return False

        except subprocess.CalledProcessError as e:
            print(f"❌ Docker启动失败: {e}")
            return False

    def start_local_services(self):
        """使用本地开发模式启动服务"""
        # 启动数据库 (如果有的话)
        print("🗄️ 请确保MySQL服务正在运行...")

        # 启动后端服务
        print("🐍 启动后端服务...")
        backend_script = f"""
import os
import sys
sys.path.insert(0, r'{self.backend_dir}')

# 设置环境变量
os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = 'mysql+mysqlconnector://root:password@localhost/wellness_platform_db'

# 启动应用
from app import app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""

        backend_script_path = self.backend_dir / "start_server.py"
        with open(backend_script_path, 'w', encoding='utf-8') as f:
            f.write(backend_script)

        # 启动前端服务
        print("🎨 启动前端服务...")

        return True

    def open_browser(self):
        """打开浏览器访问应用"""
        print("\n🌐 打开浏览器...")

        # 等待服务完全启动
        time.sleep(5)

        try:
            # 打开前端页面
            webbrowser.open("http://localhost:8080")
            print("✅ 浏览器已打开，访问: http://localhost:8080")

            # 提示API文档地址
            print("📚 API文档: http://localhost:5000")
            print("🗄️ 数据库: localhost:3306")

        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")
            print("请手动访问: http://localhost:8080")

    def cleanup(self):
        """清理临时文件"""
        print("\n🧹 清理临时文件...")

        # 删除临时启动脚本
        backend_script = self.backend_dir / "start_server.py"
        if backend_script.exists():
            backend_script.unlink()

        print("✅ 清理完成")

    def run(self):
        """主运行函数"""
        try:
            # 打印横幅
            self.print_banner()

            # 检查要求
            if not self.check_requirements():
                print("\n❌ 系统要求检查失败，请安装必要的依赖")
                return

            # 检查项目文件
            if not self.check_project_files():
                print("\n❌ 项目文件不完整")
                return

            # 设置后端
            if not self.setup_backend():
                print("\n❌ 后端设置失败")
                return

            # 设置前端
            if not self.setup_frontend():
                print("\n❌ 前端设置失败")
                return

            # 启动服务
            if not self.start_services():
                print("\n❌ 服务启动失败")
                return

            # 打开浏览器
            self.open_browser()

            print("\n" + "="*60)
            print("🎉 芝栖养生平台启动成功!")
            print("="*60)
            print("\n📱 前端应用: http://localhost:8080")
            print("🔗 后端API:  http://localhost:5000")
            print("📚 API文档:  http://localhost:5000 (Swagger UI)")
            print("\n按 Ctrl+C 停止服务")
            print("="*60)

            # 保持运行
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 正在停止服务...")
                self.cleanup()
                print("👋 感谢使用芝栖养生平台！")

        except KeyboardInterrupt:
            print("\n\n🛑 用户中断")
            self.cleanup()
        except Exception as e:
            print(f"\n❌ 启动过程中发生错误: {e}")
            self.cleanup()
            sys.exit(1)


def main():
    """主函数"""
    launcher = WellnessPlatformLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
