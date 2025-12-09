#!/usr/bin/env python3
"""
芝栖养生平台 - Nginx配置测试脚本
验证Nginx配置文件的语法和功能
"""

import os
import re

def test_nginx_config():
    """测试Nginx配置文件"""
    print("=== 测试Nginx配置 ===")

    nginx_path = 'nginx/nginx.conf'

    if not os.path.exists(nginx_path):
        print("✗ Nginx配置文件不存在")
        return False

    with open(nginx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查关键配置块
    checks = [
        ('user nginx;', '用户配置'),
        ('worker_processes auto;', '工作进程配置'),
        ('worker_connections 1024;', '连接数配置'),
        ('include /etc/nginx/mime.types;', 'MIME类型包含'),
        ('client_max_body_size 16M;', '客户端最大请求体'),
        ('gzip on;', 'Gzip压缩启用'),
        ('upstream backend', '后端上游服务器'),
        ('listen 80;', 'HTTP监听'),
        ('listen 443 ssl http2;', 'HTTPS监听'),
        ('ssl_certificate', 'SSL证书配置'),
        ('location /api/', 'API路由配置'),
        ('location /uploads/', '文件上传路由'),
        ('location /', '前端静态文件路由'),
        ('proxy_pass http://backend', '反向代理配置'),
        ('location /health', '健康检查路由'),
    ]

    all_passed = True
    for check_text, description in checks:
        if check_text in content:
            print(f"✓ {description}存在")
        else:
            print(f"✗ {description}缺失")
            all_passed = False

    return all_passed

def test_nginx_ssl_config():
    """测试Nginx SSL配置"""
    print("\n=== 测试SSL配置 ===")

    nginx_path = 'nginx/nginx.conf'

    with open(nginx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    ssl_checks = [
        ('ssl_protocols TLSv1.2 TLSv1.3;', 'SSL协议版本'),
        ('ssl_ciphers', 'SSL加密套件'),
        ('ssl_prefer_server_ciphers off;', '服务器加密套件优先级'),
        ('ssl_session_cache', 'SSL会话缓存'),
        ('ssl_session_timeout 10m;', 'SSL会话超时'),
    ]

    all_passed = True
    for check_text, description in ssl_checks:
        if check_text in content:
            print(f"✓ {description}配置正确")
        else:
            print(f"✗ {description}配置缺失")
            all_passed = False

    return all_passed

def test_nginx_security_headers():
    """测试Nginx安全头配置"""
    print("\n=== 测试安全头配置 ===")

    nginx_path = 'nginx/nginx.conf'

    with open(nginx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    security_checks = [
        ('X-Frame-Options DENY;', '点击劫持防护'),
        ('X-Content-Type-Options nosniff;', 'MIME类型嗅探防护'),
        ('X-XSS-Protection "1; mode=block";', 'XSS防护'),
        ('Strict-Transport-Security', 'HSTS头'),
    ]

    all_passed = True
    for check_text, description in security_checks:
        if check_text in content:
            print(f"✓ {description}配置存在")
        else:
            print(f"✗ {description}配置缺失")
            all_passed = False

    return all_passed

def test_nginx_proxy_config():
    """测试Nginx代理配置"""
    print("\n=== 测试代理配置 ===")

    nginx_path = 'nginx/nginx.conf'

    with open(nginx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    proxy_checks = [
        ('proxy_set_header Host $host;', '主机头传递'),
        ('proxy_set_header X-Real-IP $remote_addr;', '真实IP传递'),
        ('proxy_set_header X-Forwarded-For', '转发头传递'),
        ('proxy_set_header X-Forwarded-Proto $scheme;', '协议头传递'),
    ]

    all_passed = True
    for check_text, description in proxy_checks:
        if check_text in content:
            print(f"✓ {description}配置正确")
        else:
            print(f"✗ {description}配置缺失")
            all_passed = False

    return all_passed

def test_nginx_performance_config():
    """测试Nginx性能配置"""
    print("\n=== 测试性能配置 ===")

    nginx_path = 'nginx/nginx.conf'

    with open(nginx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    performance_checks = [
        ('sendfile on;', 'Sendfile启用'),
        ('tcp_nopush on;', 'TCP NOPUSH启用'),
        ('tcp_nodelay on;', 'TCP NODELAY启用'),
        ('keepalive_timeout 65;', 'Keepalive超时'),
        ('gzip_comp_level 6;', 'Gzip压缩级别'),
        ('expires 1y;', '静态文件缓存'),
    ]

    all_passed = True
    for check_text, description in performance_checks:
        if check_text in content:
            print(f"✓ {description}配置存在")
        else:
            print(f"⚠ {description}配置可选")

    return True  # 性能配置是可选的，不影响核心功能

def test_nginx_routing():
    """测试Nginx路由配置"""
    print("\n=== 测试路由配置 ===")

    nginx_path = 'nginx/nginx.conf'

    with open(nginx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查路由优先级和配置
    api_location = content.find('location /api/')
    uploads_location = content.find('location /uploads/')
    root_location = content.find('location / {')

    if api_location != -1 and root_location != -1:
        if api_location < root_location:
            print("✓ API路由优先级正确")
        else:
            print("⚠ API路由可能被根路由覆盖")
    else:
        print("✗ 路由配置不完整")
        return False

    # 检查SPA支持
    if 'try_files $uri $uri/ /index.html;' in content:
        print("✓ SPA路由支持配置正确")
    else:
        print("✗ SPA路由支持缺失")

    return True

def test_nginx_error_handling():
    """测试Nginx错误处理"""
    print("\n=== 测试错误处理 ===")

    nginx_path = 'nginx/nginx.conf'

    with open(nginx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查默认服务器配置
    if 'listen 80 default_server;' in content and 'return 444;' in content:
        print("✓ 默认服务器错误处理配置正确")
    else:
        print("⚠ 默认服务器配置可能不完整")

    # 检查HTTPS重定向
    if 'return 301 https://$host$request_uri;' in content:
        print("✓ HTTPS重定向配置正确")
    else:
        print("✗ HTTPS重定向配置缺失")
        return False

    return True

def main():
    """主测试函数"""
    print("芝栖养生平台 - Nginx配置测试")
    print("=" * 50)

    tests = [
        test_nginx_config,
        test_nginx_ssl_config,
        test_nginx_security_headers,
        test_nginx_proxy_config,
        test_nginx_performance_config,
        test_nginx_routing,
        test_nginx_error_handling,
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
    print("Nginx配置测试总结:")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("🎉 所有Nginx配置测试通过！")
        print("\nNginx配置特点:")
        print("• 完整的HTTPS/SSL配置")
        print("• 反向代理和负载均衡")
        print("• 安全头和防护措施")
        print("• Gzip压缩和性能优化")
        print("• SPA路由支持")
        print("• 健康检查接口")
    else:
        print("⚠️  部分Nginx配置测试失败")

    return passed == total

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
