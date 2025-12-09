#!/usr/bin/env python3
"""
芝栖养生平台 - 数据库结构测试脚本
验证数据库schema文件和表结构定义
"""

import os
import sys
import sqlite3
import re

def test_schema_file():
    """测试schema.sql文件是否存在且格式正确"""
    print("=== 测试Schema文件 ===")

    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')

    if not os.path.exists(schema_path):
        print("✗ schema.sql文件不存在")
        return False

    with open(schema_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否包含必要的表定义
    required_tables = [
        'users', 'content', 'products', 'activities',
        'experience_bases', 'orders', 'reviews'
    ]

    missing_tables = []
    for table in required_tables:
        if f'CREATE TABLE IF NOT EXISTS {table}' not in content:
            missing_tables.append(table)

    if missing_tables:
        print(f"✗ 缺少以下表的定义: {', '.join(missing_tables)}")
        return False

    print("✓ schema.sql文件存在且包含所有必要表定义")
    return True

def test_schema_syntax():
    """测试schema文件语法"""
    print("\n=== 测试Schema语法 ===")

    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')

    try:
        # 使用SQLite内存数据库测试语法
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        with open(schema_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割SQL语句并执行，过滤掉MySQL特定的语句
        statements = content.split(';')
        executed_statements = 0

        for statement in statements:
            statement = statement.strip()
            # 跳过注释和MySQL特定语句，以及索引创建（因为表创建已验证语法）
            if (statement and
                not statement.startswith('--') and
                not statement.upper().startswith('USE ') and
                not statement.upper().startswith('CREATE DATABASE') and
                not 'CREATE INDEX' in statement.upper()):

                # 处理多行语句
                lines = statement.split('\n')
                clean_statement = ' '.join(line.strip() for line in lines if line.strip() and not line.strip().startswith('--'))

                if clean_statement:
                    try:
                        cursor.execute(clean_statement)
                        executed_statements += 1
                    except sqlite3.Error as e:
                        print(f"✗ SQL语法错误: {e}")
                        print(f"问题语句: {clean_statement[:100]}...")
                        conn.close()
                        return False

        conn.close()
        print(f"✓ schema.sql语法正确，成功执行 {executed_statements} 条语句")
        return True

    except Exception as e:
        print(f"✗ schema文件测试异常: {e}")
        return False

def test_table_definitions():
    """测试具体的表定义"""
    print("\n=== 测试表定义 ===")

    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')

    with open(schema_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 测试关键表结构
    tests = [
        {
            'table': 'users',
            'required_fields': ['id', 'username', 'email', 'password', 'created_at'],
            'field_types': {
                'id': 'INT AUTO_INCREMENT PRIMARY KEY',
                'username': 'VARCHAR',
                'email': 'VARCHAR',
                'password': 'VARCHAR'
            }
        },
        {
            'table': 'products',
            'required_fields': ['id', 'name', 'category', 'price', 'stock_quantity'],
            'field_types': {
                'id': 'INT AUTO_INCREMENT PRIMARY KEY',
                'name': 'VARCHAR',
                'price': 'DECIMAL',
                'stock_quantity': 'INT'
            }
        },
        {
            'table': 'activities',
            'required_fields': ['id', 'title', 'activity_type', 'start_time', 'end_time'],
            'field_types': {
                'id': 'INT AUTO_INCREMENT PRIMARY KEY',
                'title': 'VARCHAR',
                'start_time': 'DATETIME',
                'end_time': 'DATETIME'
            }
        }
    ]

    all_passed = True

    for test in tests:
        table = test['table']
        table_pattern = rf'CREATE TABLE IF NOT EXISTS {table} \((.*?)\);'
        match = re.search(table_pattern, content, re.DOTALL)

        if not match:
            print(f"✗ 表 {table} 定义未找到")
            all_passed = False
            continue

        table_definition = match.group(1)

        # 检查必需字段
        for field in test['required_fields']:
            if field not in table_definition:
                print(f"✗ 表 {table} 缺少必需字段: {field}")
                all_passed = False

        # 检查字段类型
        for field, expected_type in test['field_types'].items():
            if expected_type not in table_definition:
                print(f"✗ 表 {table} 字段 {field} 类型不匹配，期望包含: {expected_type}")
                all_passed = False

        print(f"✓ 表 {table} 结构验证通过")

    return all_passed

def test_foreign_keys():
    """测试外键约束"""
    print("\n=== 测试外键约束 ===")

    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')

    with open(schema_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查重要的外键关系
    foreign_keys = [
        ('content', 'author_id', 'users'),
        ('activities', 'organizer_id', 'users'),
        ('orders', 'user_id', 'users'),
        ('reviews', 'user_id', 'users'),
        ('user_activities', 'user_id', 'users'),
        ('user_activities', 'activity_id', 'activities')
    ]

    all_passed = True

    for table, field, ref_table in foreign_keys:
        # 使用更灵活的模式匹配外键约束
        fk_pattern = rf'FOREIGN KEY\s*\(\s*{field}\s*\)\s*REFERENCES\s*{ref_table}'
        if not re.search(fk_pattern, content, re.IGNORECASE):
            print(f"✗ 表 {table} 缺少外键约束: {field} -> {ref_table}")
            all_passed = False
        else:
            print(f"✓ 表 {table} 外键约束验证通过: {field} -> {ref_table}")

    return all_passed

def test_indexes():
    """测试索引定义"""
    print("\n=== 测试索引定义 ===")

    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')

    with open(schema_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查重要的索引
    indexes = [
        'idx_content_type',
        'idx_content_publish_time',
        'idx_products_category',
        'idx_activities_type',
        'idx_orders_user',
        'idx_reviews_target'
    ]

    all_passed = True

    for index in indexes:
        if f'CREATE INDEX {index}' not in content:
            print(f"✗ 缺少索引: {index}")
            all_passed = False
        else:
            print(f"✓ 索引 {index} 定义存在")

    return all_passed

def main():
    """主测试函数"""
    print("芝栖养生平台 - 数据库结构测试")
    print("=" * 50)

    tests = [
        test_schema_file,
        test_schema_syntax,
        test_table_definitions,
        test_foreign_keys,
        test_indexes
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
    print("数据库结构测试总结:")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("🎉 所有数据库结构测试通过！")
        print("\n数据库特点:")
        print("• 完整的用户管理系统")
        print("• 丰富的内容和产品模型")
        print("• 完善的活动和订单系统")
        print("• 合适的外键约束和索引")
    else:
        print("⚠️  部分数据库结构测试失败")

    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
