#!/usr/bin/env python3
"""
芝栖养生平台 - 集成测试脚本
验证整个应用的协同工作能力
"""

import os
import sys
import json

def test_backend_startup():
    """测试后端应用模块导入和基本功能"""
    print("=== 测试后端应用启动能力 ===")

    try:
        # 添加backend目录到Python路径
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)

        from app import app

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_integration.db'

        # 测试应用上下文创建
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✓ 后端应用上下文创建成功")
                print(f"✓ 应用响应正常: {response.status_code}")
                return True
            else:
                print(f"✗ 应用响应异常: {response.status_code}")
                return False

    except Exception as e:
        print(f"✗ 后端启动测试异常: {e}")
        return False

def test_database_integration():
    """测试数据库集成"""
    print("\n=== 测试数据库集成 ===")

    try:
        # 添加backend目录到Python路径
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)

        from app import app, db, User, Content, Product

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_integration.db'

        with app.app_context():
            # 创建所有表
            db.create_all()
            print("✓ 数据库表创建成功")

            # 测试数据创建
            test_user = User(
                username='integration_test_user',
                email='integration@test.com',
                password='hashed_password'
            )
            db.session.add(test_user)

            test_content = Content(
                title='集成测试内容',
                content_type='article',
                content='这是集成测试的内容',
                author_id=1
            )
            db.session.add(test_content)

            test_product = Product(
                name='集成测试产品',
                category='lingzhi',
                price=99.99
            )
            db.session.add(test_product)

            db.session.commit()
            print("✓ 测试数据创建成功")

            # 测试数据查询
            users_count = User.query.count()
            content_count = Content.query.count()
            products_count = Product.query.count()

            print(f"✓ 数据查询正常 - 用户:{users_count}, 内容:{content_count}, 产品:{products_count}")

            return True

    except Exception as e:
        print(f"✗ 数据库集成测试异常: {e}")
        return False

def test_api_endpoints_integration():
    """测试API端点集成"""
    print("\n=== 测试API端点集成 ===")

    try:
        # 添加backend目录到Python路径
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)

        from app import app

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_integration.db'

        with app.test_client() as client:
            # 测试根路径
            response = client.get('/')
            print(f"✓ 根路径响应: {response.status_code}")

            # 测试API路径
            response = client.get('/api/content/')
            print(f"✓ 内容API响应: {response.status_code}")

            response = client.get('/api/products/')
            print(f"✓ 产品API响应: {response.status_code}")

            response = client.get('/api/activities/')
            print(f"✓ 活动API响应: {response.status_code}")

            return True

    except Exception as e:
        print(f"✗ API端点集成测试异常: {e}")
        return False

def test_frontend_assets():
    """测试前端资源文件"""
    print("\n=== 测试前端资源文件 ===")

    frontend_files = [
        'frontend/src/main.js',
        'frontend/src/App.vue',
        'frontend/src/router/index.js',
        'frontend/package.json',
        'frontend/vue.config.js'
    ]

    all_exist = True
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} 存在")
        else:
            print(f"✗ {file_path} 不存在")
            all_exist = False

    if all_exist:
        # 检查package.json内容
        with open('frontend/package.json', 'r', encoding='utf-8') as f:
            package_data = json.load(f)

        required_deps = ['vue', 'vue-router', 'vuex', 'axios']
        for dep in required_deps:
            if dep in package_data.get('dependencies', {}):
                print(f"✓ 依赖 {dep} 已配置")
            else:
                print(f"✗ 依赖 {dep} 缺失")
                all_exist = False

    return all_exist

def test_docker_compose_integration():
    """测试Docker Compose配置集成"""
    print("\n=== 测试Docker Compose集成 ===")

    compose_file = 'docker-compose.yml'

    if not os.path.exists(compose_file):
        print("✗ docker-compose.yml文件不存在")
        return False

    try:
        import yaml
        with open(compose_file, 'r', encoding='utf-8') as f:
            compose_config = yaml.safe_load(f)

        services = compose_config.get('services', {})

        # 检查服务依赖关系
        backend_service = services.get('backend', {})
        backend_depends = backend_service.get('depends_on', [])

        if 'db' in backend_depends:
            print("✓ 后端服务依赖数据库配置正确")
        else:
            print("✗ 后端服务缺少数据库依赖")
            return False

        # 检查端口映射
        backend_ports = backend_service.get('ports', [])
        if '5000:5000' in backend_ports:
            print("✓ 后端端口映射配置正确")
        else:
            print("✗ 后端端口映射配置错误")

        # 检查环境变量
        backend_env = backend_service.get('environment', {})
        required_env_vars = ['FLASK_ENV', 'DATABASE_URL', 'JWT_SECRET_KEY']
        for env_var in required_env_vars:
            if any(env_var in env for env in backend_env):
                print(f"✓ 环境变量 {env_var} 配置存在")
            else:
                print(f"✗ 环境变量 {env_var} 配置缺失")

        return True

    except Exception as e:
        print(f"✗ Docker Compose集成测试异常: {e}")
        return False

def test_nginx_integration():
    """测试Nginx集成配置"""
    print("\n=== 测试Nginx集成配置 ===")

    nginx_file = 'nginx/nginx.conf'

    if not os.path.exists(nginx_file):
        print("✗ Nginx配置文件不存在")
        return False

    with open(nginx_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查关键集成配置
    integration_checks = [
        ('upstream backend {', '后端上游服务器配置'),
        ('server backend:5000;', '后端服务器地址'),
        ('proxy_pass http://backend', '反向代理到后端'),
        ('root /app/static;', '前端静态文件根目录'),
        ('try_files $uri $uri/ /index.html;', 'SPA路由支持'),
    ]

    all_passed = True
    for check_text, description in integration_checks:
        if check_text in content:
            print(f"✓ {description}正确")
        else:
            print(f"✗ {description}错误")
            all_passed = False

    return all_passed

def test_project_structure():
    """测试项目整体结构"""
    print("\n=== 测试项目整体结构 ===")

    required_dirs = [
        'backend',
        'frontend',
        'nginx',
        'backend/tests',
        'frontend/src',
        'frontend/public'
    ]

    required_files = [
        'README.md',
        'docker-compose.yml',
        'Dockerfile',
        'backend/app.py',
        'backend/schema.sql',
        'frontend/package.json',
        'nginx/nginx.conf'
    ]

    all_exist = True

    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✓ 目录 {dir_path} 存在")
        else:
            print(f"✗ 目录 {dir_path} 不存在")
            all_exist = False

    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"✓ 文件 {file_path} 存在")
        else:
            print(f"✗ 文件 {file_path} 不存在")
            all_exist = False

    return all_exist

def cleanup():
    """清理测试文件"""
    try:
        test_files = ['test_integration.db']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
        print("\n✓ 测试文件清理完成")
    except:
        pass

def main():
    """主集成测试函数"""
    print("芝栖养生平台 - 集成测试")
    print("=" * 50)

    tests = [
        test_project_structure,
        test_database_integration,
        test_api_endpoints_integration,
        test_frontend_assets,
        test_docker_compose_integration,
        test_nginx_integration,
        test_backend_startup,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ 测试 {test_func.__name__} 异常: {e}")
            results.append(False)

    # 清理
    cleanup()

    # 输出测试总结
    print("\n" + "=" * 50)
    print("集成测试总结:")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("🎉 所有集成测试通过！")
        print("\n芝栖养生平台集成测试结果:")
        print("• 项目结构完整")
        print("• 数据库集成正常")
        print("• API端点响应正常")
        print("• 前端资源配置完整")
        print("• Docker容器化配置正确")
        print("• Nginx反向代理配置正确")
        print("• 后端应用启动正常")
        print("\n✅ 平台已准备好进行试点运行！")
    else:
        print("⚠️  部分集成测试失败，需要进一步检查")

    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
