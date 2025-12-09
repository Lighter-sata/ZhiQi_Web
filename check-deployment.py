#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
芝栖养生平台 - 部署检查脚本
检查生产环境的部署状态和服务健康情况
"""

import requests
import sys
import time
from urllib.parse import urljoin

class DeploymentChecker:
    def __init__(self, domain="localhost:5000"):
        self.domain = domain.rstrip('/')
        self.base_url = f"http://{domain}"
        if domain.startswith(('http://', 'https://')):
            self.base_url = domain

        # 检查结果
        self.results = {
            'domain_accessible': False,
            'api_health': False,
            'database_connection': False,
            'frontend_loaded': False,
            'ssl_certificate': False,
            'static_files': False,
            'api_endpoints': False
        }

    def print_header(self, text):
        """打印标题"""
        print(f"\n{'='*60}")
        print(f"🔍 {text}")
        print('='*60)

    def print_result(self, check_name, status, message=""):
        """打印检查结果"""
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name}: {'通过' if status else '失败'}")
        if message:
            print(f"   {message}")

    def check_domain_accessible(self):
        """检查域名是否可访问"""
        self.print_header("检查域名可访问性")

        try:
            response = requests.get(self.base_url, timeout=10)
            self.results['domain_accessible'] = response.status_code < 400
            self.print_result("域名访问", self.results['domain_accessible'],
                            f"状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.results['domain_accessible'] = False
            self.print_result("域名访问", False, f"错误: {str(e)}")

    def check_ssl_certificate(self):
        """检查SSL证书"""
        if not self.base_url.startswith('https://'):
            self.print_result("SSL证书", True, "跳过 (HTTP环境)")
            return

        self.print_header("检查SSL证书")

        try:
            response = requests.get(self.base_url, timeout=10, verify=True)
            self.results['ssl_certificate'] = True
            self.print_result("SSL证书", True, "证书有效")
        except requests.exceptions.SSLError as e:
            self.results['ssl_certificate'] = False
            self.print_result("SSL证书", False, f"证书错误: {str(e)}")
        except requests.exceptions.RequestException as e:
            self.results['ssl_certificate'] = False
            self.print_result("SSL证书", False, f"请求错误: {str(e)}")

    def check_api_health(self):
        """检查API健康状态"""
        self.print_header("检查API健康状态")

        health_url = urljoin(self.base_url, '/api/health')

        try:
            response = requests.get(health_url, timeout=10)
            is_healthy = response.status_code == 200

            self.results['api_health'] = is_healthy
            self.print_result("API健康检查", is_healthy,
                            f"状态码: {response.status_code}")

            if is_healthy:
                try:
                    data = response.json()
                    print(f"   响应: {data}")
                except:
                    print(f"   响应: {response.text[:100]}...")

        except requests.exceptions.RequestException as e:
            self.results['api_health'] = False
            self.print_result("API健康检查", False, f"错误: {str(e)}")

    def check_frontend_loaded(self):
        """检查前端是否正常加载"""
        self.print_header("检查前端页面")

        try:
            response = requests.get(self.base_url, timeout=10)
            content = response.text

            # 检查关键元素
            checks = [
                ('HTML结构', '<!DOCTYPE html>' in content),
                ('Vue应用', 'id="app"' in content),
                ('标题', '芝栖养生平台' in content),
                ('静态资源', 'css' in content or 'js' in content)
            ]

            frontend_ok = all(result for _, result in checks)
            self.results['frontend_loaded'] = frontend_ok

            self.print_result("前端加载", frontend_ok)

            for check_name, result in checks:
                status = "✅" if result else "❌"
                print(f"   {status} {check_name}")

        except requests.exceptions.RequestException as e:
            self.results['frontend_loaded'] = False
            self.print_result("前端加载", False, f"错误: {str(e)}")

    def check_static_files(self):
        """检查静态文件访问"""
        self.print_header("检查静态文件")

        static_checks = [
            ('CSS文件', '/css/', 'text/css'),
            ('JS文件', '/js/', 'application/javascript'),
            ('图片文件', '/img/', 'image/')
        ]

        static_ok = False
        for name, path, content_type in static_checks:
            try:
                url = urljoin(self.base_url, path)
                response = requests.head(url, timeout=5)

                if response.status_code == 200:
                    static_ok = True
                    self.print_result(f"{name}访问", True)
                    break
            except:
                continue

        if not static_ok:
            self.print_result("静态文件访问", False, "无法访问静态资源")

        self.results['static_files'] = static_ok

    def check_api_endpoints(self):
        """检查主要API端点"""
        self.print_header("检查API端点")

        endpoints = [
            ('内容列表', '/api/content/', 'GET'),
            ('产品列表', '/api/products/', 'GET'),
            ('活动列表', '/api/activities/', 'GET'),
            ('用户认证', '/api/auth/login', 'POST')
        ]

        api_ok = True
        for name, path, method in endpoints:
            try:
                url = urljoin(self.base_url, path)

                if method == 'GET':
                    response = requests.get(url, timeout=5)
                else:
                    # 对于POST请求，只检查端点是否存在
                    response = requests.options(url, timeout=5)

                endpoint_ok = response.status_code < 500
                status_icon = "✅" if endpoint_ok else "❌"
                print(f"   {status_icon} {name}: {response.status_code}")

                if not endpoint_ok:
                    api_ok = False

            except requests.exceptions.RequestException:
                print(f"   ❌ {name}: 连接失败")
                api_ok = False

        self.results['api_endpoints'] = api_ok
        self.print_result("API端点检查", api_ok)

    def check_database_connection(self):
        """检查数据库连接 (通过API)"""
        self.print_header("检查数据库连接")

        # 尝试通过API检查数据库连接
        # 这里可以通过一个特殊的健康检查端点或者统计信息端点

        stats_url = urljoin(self.base_url, '/api/admin/stats')

        try:
            # 注意: 这个端点需要管理员权限，可能会失败
            response = requests.get(stats_url, timeout=10)

            if response.status_code == 200:
                self.results['database_connection'] = True
                self.print_result("数据库连接", True, "管理员API访问成功")
            else:
                # 如果没有权限，尝试其他方式
                self.check_db_via_content()
        except:
            self.check_db_via_content()

    def check_db_via_content(self):
        """通过内容API检查数据库"""
        content_url = urljoin(self.base_url, '/api/content/')

        try:
            response = requests.get(content_url, timeout=10)

            # 如果能获取到内容或正确的错误响应，说明数据库连接正常
            if response.status_code in [200, 401, 403]:
                self.results['database_connection'] = True
                self.print_result("数据库连接", True, "通过内容API验证")
            else:
                self.results['database_connection'] = False
                self.print_result("数据库连接", False, f"HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.results['database_connection'] = False
            self.print_result("数据库连接", False, f"连接错误: {str(e)}")

    def generate_report(self):
        """生成检查报告"""
        self.print_header("部署检查报告")

        total_checks = len(self.results)
        passed_checks = sum(1 for result in self.results.values() if result)

        print(f"检查项目总数: {total_checks}")
        print(f"通过项目数量: {passed_checks}")
        print(f"成功率: {(passed_checks/total_checks)*100:.1f}%")

        print(f"\n{'='*60}")
        print("📊 详细结果:")

        for check_name, result in self.results.items():
            status = "✅ 通过" if result else "❌ 失败"
            check_display_name = {
                'domain_accessible': '域名可访问',
                'api_health': 'API健康检查',
                'database_connection': '数据库连接',
                'frontend_loaded': '前端页面加载',
                'ssl_certificate': 'SSL证书',
                'static_files': '静态文件访问',
                'api_endpoints': 'API端点可用性'
            }.get(check_name, check_name)

            print(f"   {status} - {check_display_name}")

        print(f"\n{'='*60}")

        if passed_checks == total_checks:
            print("🎉 恭喜！所有检查都通过了，部署非常成功！")
            print("🌐 您的应用已经可以正常使用了")
        elif passed_checks >= total_checks * 0.7:
            print("✅ 大部分检查通过，部署基本成功")
            print("⚠️  有一些小问题需要注意")
        else:
            print("❌ 检查失败较多，建议检查部署配置")
            print("📖 请参考 DEPLOYMENT.md 文档进行故障排除")

        return passed_checks == total_checks

    def run_all_checks(self):
        """运行所有检查"""
        print("🚀 开始芝栖养生平台部署检查...\n")

        self.check_domain_accessible()
        self.check_ssl_certificate()
        self.check_api_health()
        self.check_frontend_loaded()
        self.check_static_files()
        self.check_api_endpoints()
        self.check_database_connection()

        return self.generate_report()

def main():
    """主函数"""
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("请输入要检查的域名或IP地址 (默认: localhost:5000): ").strip()
        if not domain:
            domain = "localhost:5000"

    print(f"🔍 将检查部署: {domain}")
    print("请确保目标服务正在运行...\n")

    checker = DeploymentChecker(domain)

    success = checker.run_all_checks()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
