#!/usr/bin/env python3
"""
芝栖养生平台 - Docker配置测试脚本
验证Docker配置文件的语法和结构
"""

import os
import yaml
import json

def test_dockerfile():
    """测试Dockerfile配置"""
    print("=== 测试Dockerfile配置 ===")

    dockerfile_path = 'Dockerfile'

    if not os.path.exists(dockerfile_path):
        print("✗ Dockerfile文件不存在")
        return False

    with open(dockerfile_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查关键配置
    checks = [
        ('FROM node:16-alpine AS frontend-builder', '前端构建阶段'),
        ('FROM python:3.9-slim AS python-base', 'Python基础镜像'),
        ('FROM python-base AS production', '生产环境阶段'),
        ('WORKDIR /app', '工作目录设置'),
        ('EXPOSE 5000', '端口暴露'),
        ('HEALTHCHECK', '健康检查'),
        ('gunicorn', '生产服务器'),
    ]

    all_passed = True
    for check_text, description in checks:
        if check_text in content:
            print(f"✓ {description}配置存在")
        else:
            print(f"✗ {description}配置缺失")
            all_passed = False

    return all_passed

def test_docker_compose():
    """测试Docker Compose配置"""
    print("\n=== 测试Docker Compose配置 ===")

    compose_path = 'docker-compose.yml'

    if not os.path.exists(compose_path):
        print("✗ docker-compose.yml文件不存在")
        return False

    try:
        with open(compose_path, 'r', encoding='utf-8') as f:
            compose_config = yaml.safe_load(f)

        # 检查版本
        if 'version' in compose_config:
            print(f"✓ Docker Compose版本: {compose_config['version']}")
        else:
            print("⚠ Docker Compose版本未指定")

        # 检查服务
        services = compose_config.get('services', {})
        expected_services = ['backend', 'frontend-dev', 'db', 'nginx', 'redis']

        for service in expected_services:
            if service in services:
                print(f"✓ 服务 {service} 已配置")
            else:
                print(f"✗ 服务 {service} 未配置")

        # 检查网络配置
        if 'networks' in compose_config:
            print("✓ 网络配置存在")
        else:
            print("✗ 网络配置缺失")

        # 检查数据卷配置
        if 'volumes' in compose_config:
            print("✓ 数据卷配置存在")
        else:
            print("✗ 数据卷配置缺失")

        return True

    except yaml.YAMLError as e:
        print(f"✗ Docker Compose YAML语法错误: {e}")
        return False

def test_frontend_dockerfile():
    """测试前端Dockerfile配置"""
    print("\n=== 测试前端Dockerfile配置 ===")

    dockerfile_path = 'frontend/Dockerfile.dev'

    if not os.path.exists(dockerfile_path):
        print("✗ 前端Dockerfile.dev文件不存在")
        return False

    with open(dockerfile_path, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = [
        ('FROM node:16-alpine', 'Node.js镜像'),
        ('npm ci', '依赖安装'),
        ('EXPOSE 8080', '开发端口'),
        ('npm', '开发服务器启动'),
    ]

    all_passed = True
    for check_text, description in checks:
        if check_text in content:
            print(f"✓ {description}配置存在")
        else:
            print(f"✗ {description}配置缺失")
            all_passed = False

    return all_passed

def test_nginx_config():
    """测试Nginx配置"""
    print("\n=== 测试Nginx配置 ===")

    nginx_path = 'nginx/nginx.conf'

    if not os.path.exists(nginx_path):
        print("✗ Nginx配置文件不存在")
        return False

    with open(nginx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = [
        ('upstream backend', '后端上游服务器'),
        ('server {', '服务器块'),
        ('listen 80', 'HTTP监听'),
        ('listen 443', 'HTTPS监听'),
        ('proxy_pass', '反向代理'),
        ('location /api/', 'API路由'),
        ('location /', '前端路由'),
    ]

    all_passed = True
    for check_text, description in checks:
        if check_text in content:
            print(f"✓ {description}配置存在")
        else:
            print(f"✗ {description}配置缺失")
            all_passed = False

    return all_passed

def test_docker_compose_services():
    """测试Docker Compose服务配置详情"""
    print("\n=== 测试Docker Compose服务详情 ===")

    compose_path = 'docker-compose.yml'

    if not os.path.exists(compose_path):
        print("✗ docker-compose.yml文件不存在")
        return False

    try:
        with open(compose_path, 'r', encoding='utf-8') as f:
            compose_config = yaml.safe_load(f)

        services = compose_config.get('services', {})

        # 检查后端服务
        if 'backend' in services:
            backend = services['backend']
            if 'build' in backend:
                print("✓ 后端服务构建配置存在")
            if 'ports' in backend and '5000:5000' in str(backend['ports']):
                print("✓ 后端端口映射正确")
            if 'environment' in backend:
                print("✓ 后端环境变量配置存在")

        # 检查数据库服务
        if 'db' in services:
            db = services['db']
            if db.get('image') == 'mysql:8.0':
                print("✓ 数据库镜像配置正确")
            if 'environment' in db:
                print("✓ 数据库环境变量配置存在")
            if 'healthcheck' in db:
                print("✓ 数据库健康检查配置存在")

        # 检查前端开发服务
        if 'frontend-dev' in services:
            frontend = services['frontend-dev']
            if 'build' in frontend:
                print("✓ 前端开发服务构建配置存在")
            if 'volumes' in frontend:
                print("✓ 前端开发服务挂载配置存在")
            if 'profiles' in frontend and 'dev' in frontend['profiles']:
                print("✓ 前端开发服务profile配置正确")

        return True

    except Exception as e:
        print(f"✗ 服务配置测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("芝栖养生平台 - Docker配置测试")
    print("=" * 50)

    tests = [
        test_dockerfile,
        test_docker_compose,
        test_frontend_dockerfile,
        test_nginx_config,
        test_docker_compose_services,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ 测试 {test_func.__name__} 异常: {e}")
            results.append(False)

    # 输出测试总结
    print("\n" + "=" * 50)
    print("Docker配置测试总结:")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("🎉 所有Docker配置测试通过！")
        print("\nDocker配置特点:")
        print("• 多阶段构建优化镜像大小")
        print("• 完整的前后端分离部署")
        print("• 数据库和缓存服务配置")
        print("• Nginx反向代理配置")
        print("• 开发和生产环境分离")
    else:
        print("⚠️  部分Docker配置测试失败")

    return passed == total

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
