# 芝栖养生平台 - 后端服务 (Flask)

[![Flask](https://img.shields.io/badge/Flask-3.1.2-lightgrey.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

这是芝栖养生平台的后端API服务，基于Flask框架构建，提供完整的RESTful API接口。

## 🏗️ 架构特性

### 技术栈
- **Web框架**: Flask 3.1.2 + Flask-RESTX
- **数据库**: MySQL 8.0 + SQLAlchemy ORM
- **认证授权**: Flask-JWT-Extended (24小时Token有效期)
- **文件上传**: 支持图片/视频上传 (16MB限制)
- **API文档**: 自动生成Swagger UI文档

### 核心功能
- ✅ **用户认证系统**: 注册、登录、JWT Token认证
- ✅ **内容管理系统**: 文章、视频、科普内容发布管理
- ✅ **产品电商系统**: 养生产品展示、分类筛选、库存管理
- ✅ **活动体验平台**: 活动发布、报名审核、服务费计算
- ✅ **实体基地预订**: 基地展示、套餐预订、虚拟导览
- ✅ **订单交易系统**: 统一订单管理、多支付方式集成
- ✅ **评论收藏系统**: 多维度评价、用户收藏管理
- ✅ **后台审核系统**: 内容审核、活动管理、数据统计

## 📊 数据模型

### 核心数据表 (15个)
| 表名 | 说明 | 关键字段 |
|------|------|----------|
| `users` | 用户基础信息 | username, email, member_level, points |
| `content` | 内容文章 | title, content_type, author_id, status |
| `products` | 养生产品 | name, category, price, trace_code |
| `activities` | 体验活动 | title, activity_type, organizer_id, status |
| `experience_bases` | 体验基地 | name, address, facilities, features |
| `base_packages` | 基地套餐 | name, price, includes, max_capacity |
| `orders` | 统一订单 | order_number, user_id, total_amount, payment_status |
| `order_items` | 订单明细 | order_id, item_type, item_id, quantity |
| `payments` | 支付记录 | order_id, payment_method, transaction_id |
| `reviews` | 评论评价 | target_type, target_id, rating, comment |
| `favorites` | 用户收藏 | user_id, target_type, target_id |
| `notifications` | 消息通知 | user_id, title, notification_type |
| `user_activities` | 活动参与 | user_id, activity_id, participation_status |
| `admin_logs` | 管理日志 | admin_id, action, target_type |

### 数据库关系图
```
User (1) ─── (N) Content/Activity/Order/Review/Favorite
   │
   ├── (N) Order ─── (N) OrderItem ─── (1) Product/Activity/Package
   │       │
   │       └── (1) Payment
   │
   ├── (N) UserActivity ─── (1) Activity
   │
   └── (N) Review/Favorite ─── (1) Product/Activity/Content/Base
```

## 🚀 快速开始

### 环境要求
- **Python**: 3.8 或更高版本
- **MySQL**: 8.0 或更高版本
- **pip**: 20.0 或更高版本

### 1. 克隆项目
```bash
git clone https://github.com/your-repo/zhiqi-wellness-platform.git
cd zhiqi-wellness-platform/backend
```

### 2. 创建虚拟环境
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置数据库
```bash
# 方法1: 修改 app.py 中的数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://your_username:your_password@localhost/wellness_platform_db'

# 方法2: 设置环境变量 (推荐)
export DATABASE_URL='mysql+mysqlconnector://user:password@localhost/wellness_platform_db'
export JWT_SECRET_KEY='your-super-secret-key-here'
```

### 5. 创建数据库
```sql
-- 登录MySQL
mysql -u your_username -p

-- 创建数据库
CREATE DATABASE wellness_platform_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 退出MySQL，执行建表脚本
mysql -u your_username -p wellness_platform_db < schema.sql
```

### 6. 运行应用
```bash
# 开发模式
python3 app.py

# 或使用Flask CLI
export FLASK_APP=app.py
flask run
```

访问 `http://localhost:5000/` 查看API文档和测试接口。

## 📚 API 接口文档

### 认证接口 (`/api/auth/`)
```http
POST /api/auth/register     # 用户注册
POST /api/auth/login        # 用户登录
GET  /api/auth/profile      # 获取用户信息 (JWT认证)
PUT  /api/auth/profile      # 更新用户信息 (JWT认证)
```

### 内容管理 (`/api/content/`)
```http
GET    /api/content/        # 获取内容列表
POST   /api/content/        # 创建内容 (JWT认证)
GET    /api/content/:id     # 获取内容详情
PUT    /api/content/:id     # 更新内容 (JWT认证)
DELETE /api/content/:id     # 删除内容 (JWT认证)
POST   /api/content/:id/like # 点赞内容 (JWT认证)
```

### 产品管理 (`/api/products/`)
```http
GET  /api/products/         # 获取产品列表 (支持分类、搜索、分页)
GET  /api/products/:id      # 获取产品详情
```

### 活动管理 (`/api/activities/`)
```http
GET    /api/activities/     # 获取活动列表
POST   /api/activities/     # 创建活动 (JWT认证)
GET    /api/activities/:id  # 获取活动详情
POST   /api/activities/:id/register # 活动报名 (JWT认证)
```

### 基地管理 (`/api/bases/`)
```http
GET  /api/bases/            # 获取基地列表
GET  /api/bases/:id         # 获取基地详情
```

### 订单管理 (`/api/orders/`)
```http
GET    /api/orders/         # 获取用户订单列表 (JWT认证)
POST   /api/orders/         # 创建订单 (JWT认证)
GET    /api/orders/:id      # 获取订单详情 (JWT认证)
POST   /api/payments/create-payment # 创建支付 (JWT认证)
```

### 评论收藏 (`/api/reviews/`, `/api/user/`)
```http
GET    /api/reviews/        # 获取评论列表
POST   /api/reviews/        # 提交评论 (JWT认证)
GET    /api/user/favorites  # 获取用户收藏 (JWT认证)
POST   /api/user/favorites  # 添加收藏 (JWT认证)
DELETE /api/user/favorites/:id # 取消收藏 (JWT认证)
```

### 后台管理 (`/api/admin/`)
```http
GET  /api/admin/stats                   # 获取统计数据 (管理员)
GET  /api/admin/activities/review       # 获取待审核活动 (管理员)
PUT  /api/admin/activities/:id/review   # 审核活动 (管理员)
GET  /api/admin/content/review          # 获取待审核内容 (管理员)
PUT  /api/admin/content/:id/publish     # 发布内容 (管理员)
```

## 🔧 配置选项

### 环境变量
| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DATABASE_URL` | `mysql+mysqlconnector://user:pass@localhost/wellness_platform_db` | 数据库连接URL |
| `JWT_SECRET_KEY` | `wellness-platform-secret-key-2024` | JWT签名密钥 |
| `FLASK_ENV` | `development` | Flask环境 (development/production) |
| `FLASK_DEBUG` | `1` | 调试模式 (1=开启, 0=关闭) |
| `FLASK_PORT` | `5000` | 服务端口 |

### 文件上传配置
- **支持格式**: PNG, JPG, JPEG, GIF, MP4, AVI, MOV
- **大小限制**: 16MB
- **存储路径**: `uploads/` 目录

## 🧪 测试

### 运行基础测试
```bash
python3 test_basic.py
```

### API测试
使用Swagger UI进行接口测试：`http://localhost:5000/`

### 数据库测试
```bash
# 检查数据库连接
python3 -c "from app import db; print('数据库连接成功' if db else '连接失败')"
```

## 🚀 部署

### 开发环境
```bash
# 直接运行
python3 app.py
```

### 生产环境 (Gunicorn + Nginx)

#### 1. 安装Gunicorn
```bash
pip install gunicorn
```

#### 2. 使用Gunicorn运行
```bash
# 4个工作进程，绑定到所有网络接口
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 3. Nginx配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads {
        alias /path/to/your/uploads;
        expires 30d;
    }
}
```

#### 4. SSL配置 (Let's Encrypt)
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com
```

### Docker部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔒 安全特性

### 数据安全
- **密码加密**: 使用Werkzeug安全哈希 (bcrypt)
- **JWT认证**: 24小时Token有效期，支持自动刷新
- **SQL注入防护**: SQLAlchemy参数化查询
- **XSS防护**: 输入数据过滤和验证

### API安全
- **请求频率限制**: 防止暴力攻击
- **CORS配置**: 跨域资源控制
- **错误处理**: 不暴露敏感信息
- **日志记录**: 管理员操作审计

### 文件安全
- **上传验证**: 文件类型和大小限制
- **路径遍历防护**: 安全文件名生成
- **存储隔离**: 上传文件与应用代码分离

## 📊 性能优化

### 数据库优化
- **索引策略**: 15个核心索引提升查询性能
- **连接池**: SQLAlchemy连接池管理
- **查询优化**: N+1问题防护，预加载关联数据

### API优化
- **分页查询**: 大数据量分页加载
- **缓存策略**: 热点数据缓存
- **异步处理**: 耗时操作异步执行

### 前端优化
- **代码分割**: Vue Router懒加载
- **资源压缩**: Gzip压缩传输
- **CDN加速**: 静态资源CDN分发

## 🐛 故障排除

### 常见问题

#### 数据库连接失败
```bash
# 检查MySQL服务状态
sudo systemctl status mysql

# 检查数据库是否存在
mysql -u root -p -e "SHOW DATABASES;"

# 重新创建数据库
mysql -u root -p < schema.sql
```

#### 端口占用
```bash
# 检查端口使用情况
lsof -i :5000

# 杀死占用进程
kill -9 <PID>
```

#### 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### JWT Token过期
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

## 📈 扩展开发

### 添加新功能
1. 在 `app.py` 中添加新的数据模型
2. 更新 `schema.sql` 数据库结构
3. 实现API接口和业务逻辑
4. 添加前端页面和路由
5. 更新文档

### 插件集成
- **邮件服务**: Flask-Mail集成
- **缓存系统**: Redis缓存层
- **消息队列**: Celery异步任务
- **监控告警**: Sentry错误追踪

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add some AmazingFeature'`
4. 推送分支: `git push origin feature/AmazingFeature`
5. 发起Pull Request

## 📄 许可证

[MIT License](LICENSE)

## 📞 技术支持

- **邮箱**: tech-support@zhiqi-wellness.com
- **文档**: [API文档](http://localhost:5000/) (启动服务后访问)
- **问题**: [GitHub Issues](https://github.com/your-repo/issues)

---

**芝栖养生平台后端服务** - 稳定可靠的API服务 🌟
