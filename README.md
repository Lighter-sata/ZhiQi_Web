# 芝栖养生平台

[![Vue.js](https://img.shields.io/badge/Vue.js-3.2.13-brightgreen.svg)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-lightgrey.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🌿 **连接自然之力，引领品质生活** 🌿

芝栖养生平台是一个基于Vue.js 3 + Flask的现代化全栈Web应用，实现内容营销、产品电商、活动体验、实体基地为一体的综合性养生健康平台。

---

## 📋 目录

- [🔧 功能集成](#-功能集成)
- [📁 项目文件结构](#-项目文件结构)
- [🚀 使用方法](#-使用方法)
- [🏗️ 技术架构](#️-技术架构)
- [📊 数据模型](#-数据模型)
- [🔒 安全特性](#-安全特性)
- [📈 部署运维](#-部署运维)
- [🤝 贡献指南](#-贡献指南)
- [🚀 部署运维](./DEPLOYMENT.md)
- [📞 联系我们](#-联系我们)

---

## 🔧 功能集成

### 🎯 核心业务模块

#### **1. 用户管理系统**
- ✅ 用户注册/登录/退出
- ✅ JWT身份认证和权限控制
- ✅ 用户资料管理 (头像、个人信息、会员等级)
- ✅ 积分系统和会员权益
- ✅ 密码重置和安全设置

#### **2. 内容管理系统**
- ✅ 多类型内容支持 (文章、视频、科普、Vlog)
- ✅ 内容发布、编辑、删除
- ✅ 标签分类和搜索功能
- ✅ 内容审核和发布流程
- ✅ 阅读量统计和热门排行

#### **3. 产品电商系统**
- ✅ 产品展示和分类管理
- ✅ 购物车和收藏功能
- ✅ 订单创建和管理
- ✅ 库存管理和价格策略
- ✅ 产品评价和评分系统

#### **4. 活动体验平台**
- ✅ 官方活动发布和管理
- ✅ 用户活动发布 (需审核)
- ✅ 活动报名和参与跟踪
- ✅ 活动评价和反馈收集
- ✅ 平台服务费自动计算 (10-20%)

#### **5. 实体体验基地**
- ✅ 基地信息展示和介绍
- ✅ 套餐服务和价格管理
- ✅ 在线预订和预约系统
- ✅ 虚拟导览和图片展示
- ✅ 基地评价和用户反馈

#### **6. 支付结算系统**
- ✅ **微信支付集成**: 扫码支付、回调处理
- ✅ **支付宝集成**: 网页支付、异步通知
- ✅ 支付状态实时查询
- ✅ 订单自动状态更新
- ✅ 交易记录和对账功能

#### **7. 数据分析面板**
- ✅ **销售分析**: 每日销售额趋势图、产品销售排行
- ✅ **用户行为**: 注册趋势、活跃度分析、会员分布
- ✅ **收入统计**: 月度收入、收入来源、平台收益
- ✅ **实时监控**: 可视化图表、数据导出

#### **8. 后台管理系统**
- ✅ 用户管理 (查看、编辑、禁用)
- ✅ 内容审核和发布管理
- ✅ 订单处理和发货管理
- ✅ 活动审核和状态管理
- ✅ 系统配置和参数设置

### 🛠️ 技术集成

#### **前端技术栈**
- **Vue.js 3**: 组合式API、响应式数据绑定
- **Vue Router 4**: 单页面应用路由管理
- **Vuex 4**: 集中式状态管理
- **Axios**: HTTP客户端和API调用
- **SCSS**: 样式预处理器和设计系统

#### **后端技术栈**
- **Flask 3**: 轻量级Web框架
- **Flask-SQLAlchemy**: ORM数据映射
- **Flask-JWT-Extended**: JWT认证扩展
- **Flask-RESTX**: RESTful API构建
- **MySQL**: 关系型数据库

#### **支付集成**
- **微信支付**: 官方SDK集成，支持扫码支付
- **支付宝**: 官方SDK集成，支持网页支付
- **回调处理**: 异步通知和状态同步
- **安全保障**: 签名验证和数据加密

#### **部署集成**
- **Docker**: 容器化部署和环境隔离
- **Nginx**: 反向代理和静态文件服务
- **CI/CD**: GitHub Actions自动化流水线
- **监控**: 健康检查和日志收集

---

## 📁 项目文件结构

```
芝栖养生平台/
├── backend/                    # 🐍 Flask后端服务
│   ├── app.py                  # 主应用文件 (1972行)
│   ├── schema.sql             # 🗄️ 数据库结构 (257行)
│   ├── requirements.txt       # 📦 Python依赖包
│   ├── test_basic.py          # 🧪 基础测试脚本
│   └── tests/                 # 🧪 后端测试用例
│       ├── test_api.py        # API接口测试
│       └── test_payment.py    # 💳 支付功能测试
├── frontend/                  # 🎨 Vue.js前端应用
│   ├── src/                   # 📁 源代码目录
│   │   ├── main.js           # 🚀 Vue应用入口
│   │   ├── App.vue           # 🎯 根组件 (导航+路由)
│   │   ├── router/           # 🧭 路由配置
│   │   │   └── index.js      # 页面路由定义
│   │   ├── store/            # 📊 Vuex状态管理
│   │   │   └── index.js      # 全局状态管理
│   │   ├── utils/            # 🛠️ 工具函数
│   │   │   ├── api.js        # 🔗 HTTP客户端封装
│   │   │   └── validators.js # ✅ 表单验证工具
│   │   ├── styles/           # 🎨 样式文件
│   │   │   ├── variables.scss # 🎨 设计变量
│   │   │   ├── mixins.scss   # 🛠️ 样式混合器
│   │   │   └── global.scss   # 🌍 全局样式
│   │   └── views/            # 📱 页面组件
│   │       ├── HomeView.vue          # 🏠 首页
│   │       ├── ContentList.vue       # 📚 内容列表页
│   │       ├── ProductList.vue       # 🛍️ 产品列表页
│   │       ├── Payment.vue           # 💳 支付页面
│   │       ├── PaymentSuccess.vue    # ✅ 支付成功页
│   │       ├── AdminAnalytics.vue    # 📊 数据分析面板
│   │       └── ...                   # 其他页面组件
│   ├── public/                # 📁 静态资源
│   │   └── index.html        # 🌐 HTML模板
│   ├── package.json          # 📦 前端依赖配置
│   ├── vue.config.js         # ⚙️ Vue CLI配置
│   └── Dockerfile.dev        # 🐳 开发环境Docker配置
├── nginx/                    # 🌐 Nginx配置
│   └── nginx.conf           # 反向代理配置
├── docker-compose.yml       # 🐳 Docker服务编排
├── Dockerfile              # 🐳 生产环境构建
├── .github/                # 🤖 CI/CD配置
│   └── workflows/
│       └── ci-cd.yml       # GitHub Actions流水线
├── .gitignore             # 🚫 Git忽略规则
└── README.md              # 📚 项目文档
```

### 📂 核心文件说明

#### **后端核心文件**
- **`backend/app.py`** - 主应用文件，包含25+个API接口、用户认证、支付集成
- **`backend/schema.sql`** - 完整的数据库表结构，15个核心业务表
- **`backend/requirements.txt`** - Python依赖包清单，包含支付SDK等
- **`backend/tests/`** - 完整的测试套件，覆盖API和支付功能

#### **前端核心文件**
- **`frontend/src/main.js`** - Vue应用入口，初始化路由和状态管理
- **`frontend/src/App.vue`** - 根组件，包含导航栏和页面布局
- **`frontend/src/router/index.js`** - 路由配置，定义所有页面路径
- **`frontend/src/store/index.js`** - Vuex状态管理，用户认证和全局状态
- **`frontend/src/utils/api.js`** - HTTP客户端，统一的API调用封装
- **`frontend/src/styles/`** - 完整的样式系统，包含设计变量和工具类

#### **部署配置文件**
- **`Dockerfile`** - 多阶段Docker构建，优化生产环境镜像
- **`docker-compose.yml`** - 服务编排，定义完整的开发/生产环境栈
- **`nginx/nginx.conf`** - 反向代理配置，支持SSL和负载均衡
- **`.github/workflows/ci-cd.yml`** - 自动化CI/CD流水线

---

## 🏗️ 技术架构

### 🏛️ 系统架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js前端    │    │   Flask后端API  │    │    MySQL数据库   │
│                 │    │                 │    │                 │
│  • 单页应用     │◄──►│  • RESTful API  │◄──►│  • 15个业务表   │
│  • 响应式设计   │    │  • JWT认证      │    │  • 数据关系     │
│  • 状态管理     │    │  • 支付集成     │    │  • 索引优化     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Nginx代理     │
                    │                 │
                    │  • 反向代理     │
                    │  • 负载均衡     │
                    │  • SSL证书      │
                    └─────────────────┘
```

### 🔧 技术栈详情

#### **后端技术栈**
- **Web框架**: Flask 3.1.2 - 轻量级Python Web框架
- **API构建**: Flask-RESTX - 自动生成Swagger文档
- **数据库ORM**: Flask-SQLAlchemy - 对象关系映射
- **认证授权**: Flask-JWT-Extended - JWT Token管理
- **支付集成**: 微信支付SDK + 支付宝SDK
- **部署服务**: Gunicorn - WSGI服务器
- **反向代理**: Nginx - 负载均衡和静态文件服务

#### **前端技术栈**
- **核心框架**: Vue.js 3.2.13 - 渐进式JavaScript框架
- **路由管理**: Vue Router 4.0.3 - 单页应用路由
- **状态管理**: Vuex 4.0.0 - 集中式状态管理
- **HTTP客户端**: Axios 1.6.0 - 基于Promise的HTTP库
- **样式系统**: SCSS - CSS预处理器 + Flexbox/Grid
- **构建工具**: Vue CLI 5.x - 零配置的前端构建工具

#### **数据库技术栈**
- **数据库**: MySQL 8.0 - 关系型数据库
- **连接驱动**: mysql-connector-python - 官方MySQL驱动
- **数据建模**: SQLAlchemy - Python SQL工具包
- **连接池**: SQLAlchemy Pool - 数据库连接池管理

#### **DevOps技术栈**
- **容器化**: Docker 20.10+ - 应用容器化
- **编排工具**: Docker Compose - 多容器应用定义
- **CI/CD**: GitHub Actions - 自动化构建和部署
- **代码质量**: ESLint + Prettier - 代码规范检查
- **版本控制**: Git - 分布式版本控制系统

### 📡 API架构设计

#### **RESTful API设计原则**
- **资源导向**: 每个资源都有唯一的URL标识
- **HTTP方法**: GET(查询)、POST(创建)、PUT(更新)、DELETE(删除)
- **状态码**: 标准HTTP状态码表示操作结果
- **数据格式**: JSON作为统一的数据交换格式

#### **API接口分类**
```javascript
// 用户认证接口
POST   /api/auth/register     // 用户注册
POST   /api/auth/login        // 用户登录
GET    /api/auth/profile      // 获取用户信息

// 内容管理接口
GET    /api/content/          // 内容列表
POST   /api/content/          // 创建内容
GET    /api/content/:id       // 内容详情

// 产品电商接口
GET    /api/products/         // 产品列表
GET    /api/products/:id      // 产品详情

// 活动平台接口
GET    /api/activities/       // 活动列表
POST   /api/activities/       // 创建活动

// 订单支付接口
POST   /api/orders/           // 创建订单
POST   /api/payments/create-payment  // 发起支付
```

### 🔐 安全架构

#### **身份认证**
- **JWT Token**: 无状态身份认证
- **密码加密**: bcrypt哈希算法
- **会话管理**: Token过期和刷新机制

#### **API安全**
- **请求验证**: 输入数据验证和过滤
- **SQL注入防护**: 参数化查询
- **XSS防护**: 前端数据转义
- **CSRF防护**: Token验证机制

#### **传输安全**
- **HTTPS**: 生产环境强制HTTPS
- **SSL证书**: Let's Encrypt免费证书
- **安全头**: HSTS、CSP等安全头配置

---

## 🚀 使用方法

### 📋 环境要求

| 组件 | 版本要求 | 说明 |
|------|----------|------|
| **Python** | 3.9+ | 后端运行环境 |
| **Node.js** | 16+ | 前端构建工具 |
| **MySQL** | 8.0+ | 数据库服务 |
| **Docker** | 20.10+ | 容器化部署 (可选) |
| **Git** | 2.0+ | 版本控制 |

### 🔧 快速开始

#### **方式一：Docker部署 (推荐)**

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/zhiqi-wellness.git
cd zhiqi-wellness

# 2. 启动完整环境
docker-compose up -d

# 3. 访问应用
# 前端: http://localhost:8080 (开发环境)
# 后端API: http://localhost:5000
# 数据库: localhost:3306
```

#### **方式二：本地开发环境**

##### **1. 后端设置**

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量 (可选)
export DATABASE_URL="mysql+mysqlconnector://user:password@localhost/wellness_platform_db"
export JWT_SECRET_KEY="your-secret-key-here"

# 启动后端服务
python3 app.py
# 服务将在 http://localhost:5000 启动
```

##### **2. 数据库初始化**

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE wellness_platform_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 应用启动时会自动创建表结构
# 或手动执行schema.sql
mysql -u root -p wellness_platform_db < schema.sql
```

##### **3. 前端设置**

```bash
# 进入前端目录
cd frontend

# 安装Node.js依赖
npm install

# 配置环境变量 (可选)
echo "VUE_APP_API_BASE_URL=http://localhost:5000" > .env.local

# 启动开发服务器
npm run serve
# 前端将在 http://localhost:8080 启动
```

### 🎯 常用命令

#### **开发命令**

```bash
# 后端开发
cd backend
python3 app.py                    # 启动Flask开发服务器
python3 -m pytest tests/ -v      # 运行后端测试

# 前端开发
cd frontend
npm run serve                    # 启动Vue开发服务器
npm run build                    # 构建生产版本
npm run lint                     # 代码检查
```

#### **Docker命令**

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 重启服务
docker-compose restart backend

# 停止所有服务
docker-compose down

# 重新构建镜像
docker-compose build --no-cache
```

#### **数据库命令**

```bash
# 连接数据库
docker-compose exec db mysql -u zhiqi_user -p wellness_platform_db
# 密码: zhiqi_password

# 备份数据库
docker-compose exec db mysqldump -u zhiqi_user -p wellness_platform_db > backup.sql

# 恢复数据库
docker-compose exec -T db mysql -u zhiqi_user -p wellness_platform_db < backup.sql
```

### ⚙️ 配置说明

#### **环境变量配置**

创建 `.env` 文件或设置系统环境变量：

```bash
# 数据库配置
DATABASE_URL=mysql+mysqlconnector://user:password@host:port/database

# JWT配置
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ACCESS_TOKEN_EXPIRES=24

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_PORT=5000

# 支付配置 (生产环境)
WECHAT_PAY_APP_ID=your_wechat_app_id
WECHAT_PAY_MCH_ID=your_merchant_id
ALIPAY_APP_ID=your_alipay_app_id

# 文件上传配置
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# 前端配置
VUE_APP_API_BASE_URL=http://localhost:5000
VUE_APP_ENV=development
```

#### **数据库配置**

```sql
-- 生产环境推荐配置
CREATE DATABASE wellness_platform_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 创建用户 (生产环境使用强密码)
CREATE USER 'zhiqi_user'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON wellness_platform_db.* TO 'zhiqi_user'@'%';
FLUSH PRIVILEGES;
```

### 🔍 API文档访问

启动后端服务后，访问以下地址查看API文档：

- **Swagger UI**: `http://localhost:5000/` - 交互式API文档
- **API列表**: 所有端点自动生成文档和测试界面

### 🧪 测试运行

```bash
# 运行后端测试
cd backend
python3 -m pytest tests/test_payment.py -v

# 运行前端测试 (如果配置了)
cd frontend
npm run test:unit
```

### 🚀 生产部署

#### **使用Docker (推荐)**

```bash
# 1. 构建生产镜像
docker build -t zhiqi-wellness:latest .

# 2. 运行生产容器
docker run -d \
  --name zhiqi-wellness \
  -p 5000:5000 \
  -e DATABASE_URL="mysql://..." \
  -e JWT_SECRET_KEY="..." \
  zhiqi-wellness:latest

# 3. 配置Nginx反向代理
# 复制nginx/nginx.conf到Nginx配置目录
```

#### **传统部署**

```bash
# 1. 构建前端静态文件
cd frontend && npm run build

# 2. 配置生产环境变量
export FLASK_ENV=production
export DATABASE_URL="mysql://..."

# 3. 使用Gunicorn启动
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app

# 4. 配置Nginx
# 设置反向代理到localhost:5000
# 配置SSL证书
```

---

## 🏗️ 技术架构

---

## 📊 数据模型

### 🗄️ 核心数据表设计 (15个表)

#### **用户管理模块**
```sql
users (用户表)
├── id (主键)
├── username (用户名，唯一)
├── password (密码哈希)
├── email (邮箱，唯一)
├── phone (手机号)
├── avatar (头像URL)
├── real_name (真实姓名)
├── member_level (会员等级: normal/vip/premium)
├── points (积分)
├── total_spent (累计消费)
├── is_active (激活状态)
└── created_at/updated_at (时间戳)
```

#### **内容管理模块**
```sql
content (内容表)
├── id (主键)
├── title (标题)
├── content (内容)
├── content_type (类型: article/video/knowledge/vlog)
├── summary (摘要)
├── cover_image (封面图)
├── author_id (作者ID)
├── status (状态: draft/published)
├── views_count (阅读量)
├── likes_count (点赞数)
└── created_at/published_at (时间戳)
```

#### **产品电商模块**
```sql
products (产品表)
├── id (主键)
├── name (产品名称)
├── description (产品描述)
├── price (价格)
├── original_price (原价)
├── stock_quantity (库存)
├── category (分类)
├── images (产品图片JSON)
├── specifications (规格JSON)
├── is_available (上架状态)
└── created_at/updated_at (时间戳)
```

#### **活动平台模块**
```sql
activities (活动表)
├── id (主键)
├── title (活动标题)
├── description (活动描述)
├── activity_type (活动类型)
├── organizer_id (组织者ID)
├── start_time/end_time (活动时间)
├── max_participants (最大参与人数)
├── current_participants (当前参与人数)
├── price (活动价格)
├── location (活动地点)
├── status (状态: pending/approved/rejected)
├── review_status (审核状态)
└── created_at/updated_at (时间戳)

user_activities (用户活动参与表)
├── id (主键)
├── user_id (用户ID)
├── activity_id (活动ID)
├── order_id (订单ID)
├── participation_status (参与状态)
└── joined_at/created_at (时间戳)
```

#### **体验基地模块**
```sql
experience_bases (基地表)
├── id (主键)
├── name (基地名称)
├── description (基地描述)
├── location (地理位置)
├── images (基地图片JSON)
├── facilities (设施JSON)
├── is_active (激活状态)
└── created_at/updated_at (时间戳)

base_packages (基地套餐表)
├── id (主键)
├── base_id (基地ID)
├── name (套餐名称)
├── description (套餐描述)
├── price (价格)
├── duration (时长/天)
├── includes (包含服务JSON)
└── is_available (可用状态)
```

#### **订单交易模块**
```sql
orders (订单表)
├── id (主键)
├── order_number (订单号，唯一)
├── user_id (用户ID)
├── order_type (订单类型: product/activity/base)
├── total_amount (总金额)
├── subtotal (小计)
├── discount_amount (优惠金额)
├── status (订单状态)
├── payment_status (支付状态)
└── created_at/paid_at (时间戳)

order_items (订单明细表)
├── id (主键)
├── order_id (订单ID)
├── item_type (商品类型)
├── item_id (商品ID)
├── item_name (商品名称)
├── quantity (数量)
├── price (单价)
└── created_at (时间戳)

payments (支付记录表)
├── id (主键)
├── order_id (订单ID)
├── payment_method (支付方式: wechat/alipay)
├── amount (支付金额)
├── transaction_id (交易号)
├── payment_status (支付状态)
├── payment_data (支付数据JSON)
└── created_at (时间戳)
```

#### **互动功能模块**
```sql
reviews (评价表)
├── id (主键)
├── user_id (用户ID)
├── item_type (评价对象类型)
├── item_id (评价对象ID)
├── rating (评分)
├── comment (评价内容)
├── images (评价图片JSON)
└── created_at (时间戳)

favorites (收藏表)
├── id (主键)
├── user_id (用户ID)
├── item_type (收藏对象类型)
├── item_id (收藏对象ID)
└── created_at (时间戳)

notifications (通知表)
├── id (主键)
├── user_id (用户ID)
├── type (通知类型)
├── title (通知标题)
├── content (通知内容)
├── is_read (已读状态)
└── created_at (时间戳)
```

#### **管理审计模块**
```sql
admin_logs (管理员日志表)
├── id (主键)
├── admin_id (管理员ID)
├── action (操作类型)
├── target_type (操作对象类型)
├── target_id (操作对象ID)
├── details (操作详情JSON)
├── ip_address (IP地址)
└── created_at (时间戳)
```

### 🔗 数据库关系图

```
用户(users) ──┬── 发布 ──► 内容(content)
           │
           ├── 参与 ──► 活动(user_activities)
           │
           ├── 下单 ──► 订单(orders) ──┬── 明细 ──► 订单项(order_items)
           │                           │
           ├── 支付 ──► 支付(payments) ◄── 关联 ── 订单(orders)
           │
           ├── 评价 ──► 评价(reviews)
           │
           ├── 收藏 ──► 收藏(favorites)
           │
           └── 接收 ──► 通知(notifications)

管理员 ─── 操作 ──► 管理日志(admin_logs)
```

### 📈 数据库优化

#### **索引策略**
- **主键索引**: 所有表的主键自动创建
- **外键索引**: 重要外键字段建立索引
- **复合索引**: 经常组合查询的字段
- **全文索引**: 内容标题和描述的搜索

#### **性能优化**
- **读写分离**: 支持数据库读写分离部署
- **连接池**: SQLAlchemy连接池管理
- **查询优化**: 避免N+1查询问题
- **缓存策略**: 热点数据缓存机制

---

## 🔒 安全特性

## 🚀 核心功能

### 1. 🏠 品牌展示系统
- **Hero区域**: 品牌故事 + 核心价值展示
- **服务矩阵**: 四大核心服务板块可视化
- **品牌文化**: 灵芝养生文化深度融合

### 2. 📚 内容营销系统
- **硬核科普**: "3分钟看懂孢子粉破壁技术"
- **生活方式**: Vlog、用户故事、体验短片
- **品牌故事**: 基地介绍、文化传承内容

### 3. 🛍️ 产品电商系统
- **产品分类**: 灵芝产品、养生茶饮、孢子粉、文创周边、订阅盒
- **智能筛选**: 分类筛选、价格排序、搜索功能
- **购物体验**: 购物车、收藏、立即购买

### 4. 🎯 活动体验平台
- **活动类型**: 工坊体验、瑜伽课程、手作活动、采摘体验
- **报名系统**: 在线报名、实时库存、支付确认
- **审核机制**: 用户活动需平台审核通过后发布

### 5. 🏞️ 实体体验基地
- **基地展示**: 接待展示区、静修住宿区、多功能工坊区、户外体验区
- **预订套餐**: "静心一夜"、"工坊周末"等标准化套餐
- **虚拟导览**: 基地环境、设施在线展示

### 6. 👤 用户中心
- **个人资料**: 基本信息、会员等级、积分显示
- **订单管理**: 产品订单、活动订单、住宿订单
- **活动参与**: 我的活动、参与记录、评价反馈
- **收藏管理**: 收藏的产品、活动、内容

### 7. ⚙️ 后台管理系统
- **内容审核**: 用户发布内容审核发布
- **活动管理**: 活动审核、状态管理、统计分析
- **订单处理**: 订单状态更新、退款处理
- **用户管理**: 用户信息、会员管理、数据统计

## 🛠️ 技术栈

### 后端技术栈
- **框架**: Flask 3.1.2 + Flask-RESTX
- **数据库**: MySQL 8.0 + SQLAlchemy ORM
- **认证**: Flask-JWT-Extended (JWT Token)
- **部署**: Gunicorn + Nginx (生产环境)

### 前端技术栈
- **框架**: Vue.js 3.2.13 + Composition API
- **路由**: Vue Router 4.0.3 (懒加载)
- **状态**: Vuex 4.0.0 (集中状态管理)
- **HTTP**: Axios 1.6.0 (请求拦截器)
- **样式**: 原生CSS + Flexbox/Grid (响应式)

### 开发工具
- **版本控制**: Git
- **API文档**: Swagger UI (自动生成)
- **代码质量**: ESLint + Prettier
- **包管理**: npm + pip

## 📋 安装和运行

### 环境要求
- **Python**: 3.8+
- **Node.js**: 14.0+
- **MySQL**: 8.0+
- **npm**: 6.0+

### 后端部署

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置数据库
# 编辑 app.py 中的数据库连接配置
# 或设置环境变量 DATABASE_URL

# 5. 运行应用
python3 app.py
```

### 前端部署

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run serve

# 4. 构建生产版本
npm run build
```

### 完整开发环境

```bash
# 终端1: 启动后端 (http://localhost:5000)
cd backend && python3 app.py

# 终端2: 启动前端 (http://localhost:8080)
cd frontend && npm run serve
```

## 🔧 配置说明

### 环境变量
```bash
# 数据库配置
DATABASE_URL=mysql+mysqlconnector://user:password@localhost/wellness_platform_db

# JWT密钥 (生产环境请使用强密钥)
JWT_SECRET_KEY=your-super-secret-key-here

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_PORT=5000
```

### 数据库初始化
```sql
-- 创建数据库
CREATE DATABASE wellness_platform_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 执行schema.sql中的建表语句
-- 应用启动时会自动创建表结构
```

## 📚 API文档

启动后端服务后，访问 `http://localhost:5000/` 查看自动生成的Swagger API文档。

### 主要API端点

#### 用户认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/profile` - 获取用户信息

#### 内容管理
- `GET /api/content/` - 内容列表
- `POST /api/content/` - 创建内容
- `GET /api/content/{id}` - 内容详情

#### 产品电商
- `GET /api/products/` - 产品列表
- `GET /api/products/{id}` - 产品详情

#### 活动平台
- `GET /api/activities/` - 活动列表
- `POST /api/activities/` - 创建活动
- `POST /api/activities/{id}/register` - 活动报名

#### 订单系统
- `POST /api/orders/` - 创建订单
- `POST /api/payments/create-payment` - 支付订单

## 🎨 设计特色

### 品牌视觉设计
- **主色调**: 灵芝棕 (#8b5a3c) + 自然绿色 (#8fbc8f)
- **设计语言**: 自然、宁静、健康、品质
- **UI组件**: 现代化卡片设计、流畅动画效果

### 响应式设计
- **移动优先**: 支持320px+宽度设备
- **断点设计**: 768px (平板), 1024px (桌面)
- **触控优化**: 移动端手势和交互

### 用户体验优化
- **加载状态**: 全局loading指示器
- **错误处理**: 友好的错误提示信息
- **无缝转化**: 内容消费 → 兴趣产生 → 立即行动

## 🔒 安全特性

### 数据安全
- **密码加密**: bcrypt哈希算法
- **JWT认证**: 无状态token验证
- **HTTPS**: 生产环境强制HTTPS

### API安全
- **请求限制**: 防止暴力攻击
- **数据验证**: 前后端双重验证
- **SQL注入防护**: 参数化查询

### 🛡️ 数据安全

#### **身份认证安全**
- **JWT Token认证**: 无状态身份验证，防止会话劫持
- **密码加密存储**: bcrypt哈希算法，防止彩虹表攻击
- **Token过期机制**: Access Token 24小时过期，自动刷新
- **多因子认证**: 支持未来扩展的2FA功能

#### **传输安全**
- **HTTPS强制**: 生产环境强制HTTPS传输
- **SSL/TLS加密**: TLS 1.2+ 协议支持
- **安全头配置**:
  ```nginx
  add_header X-Frame-Options DENY;
  add_header X-Content-Type-Options nosniff;
  add_header X-XSS-Protection "1; mode=block";
  add_header Strict-Transport-Security "max-age=31536000";
  ```

#### **数据保护**
- **敏感数据加密**: 手机号、邮箱等敏感信息加密存储
- **数据脱敏**: 日志和显示中的敏感信息脱敏处理
- **备份加密**: 数据库备份文件加密存储
- **数据保留**: 符合GDPR的数据保留政策

### 🔐 API安全

#### **请求安全**
- **输入验证**: 前后端双重数据验证
- **SQL注入防护**: SQLAlchemy参数化查询
- **XSS防护**: 前端数据转义和CSP策略
- **CSRF防护**: JWT Token防止跨站请求伪造

#### **访问控制**
- **角色权限**: 普通用户/管理员权限分离
- **API限流**: 防止恶意请求和DDoS攻击
- **审计日志**: 所有管理员操作记录追踪
- **异常监控**: 实时监控异常访问和错误

#### **文件安全**
- **上传验证**: 文件类型、大小、内容验证
- **存储安全**: 文件隔离存储，防止路径遍历
- **CDN加速**: 静态资源CDN分发，减轻服务器压力

### 👤 用户隐私保护

#### **隐私合规**
- **数据最小化**: 只收集必要的用户数据
- **同意管理**: 用户数据使用明确同意
- **删除权利**: 用户可要求删除个人数据
- **隐私政策**: 清晰的隐私政策和使用条款

#### **数据隔离**
- **用户隔离**: 用户数据物理隔离
- **权限分层**: 不同角色访问不同数据
- **日志匿名**: 操作日志中的敏感信息匿名化

---

## 📈 部署运维

### 🐳 Docker容器化部署

#### **单命令启动 (推荐)**
```bash
# 克隆项目
git clone https://github.com/your-repo/zhiqi-wellness.git
cd zhiqi-wellness

# 一键启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### **服务架构**
```yaml
services:
  backend:      # Flask API服务 (端口:5000)
  frontend-dev: # Vue开发服务器 (端口:8080)
  db:          # MySQL数据库 (端口:3306)
  nginx:       # 生产环境反向代理 (端口:80)
```

### ☸️ Kubernetes部署

#### **生产环境K8s部署**
```yaml
# 创建命名空间
kubectl create namespace zhiqi-wellness

# 部署数据库
kubectl apply -f k8s/mysql-deployment.yaml

# 部署后端服务
kubectl apply -f k8s/backend-deployment.yaml

# 部署前端服务
kubectl apply -f k8s/frontend-deployment.yaml

# 部署Nginx入口
kubectl apply -f k8s/nginx-ingress.yaml
```

### 🔧 传统部署方式

#### **生产环境手动部署**
```bash
# 1. 服务器准备
sudo apt update && sudo apt upgrade -y
sudo apt install nginx mysql-server python3-pip -y

# 2. 数据库配置
sudo mysql_secure_installation
mysql -u root -p
CREATE DATABASE wellness_platform_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'zhiqi_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON wellness_platform_db.* TO 'zhiqi_user'@'localhost';

# 3. 后端部署
cd /var/www/zhiqi-wellness/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 创建systemd服务
sudo tee /etc/systemd/system/zhiqi-backend.service > /dev/null <<EOF
[Unit]
Description=Zhiqi Wellness Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/zhiqi-wellness/backend
Environment="DATABASE_URL=mysql+mysqlconnector://zhiqi_user:password@localhost/wellness_platform_db"
Environment="JWT_SECRET_KEY=your-production-jwt-key"
ExecStart=/var/www/zhiqi-wellness/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable zhiqi-backend
sudo systemctl start zhiqi-backend

# 4. 前端部署
cd /var/www/zhiqi-wellness/frontend
npm install
npm run build

# 5. Nginx配置
sudo tee /etc/nginx/sites-available/zhiqi-wellness > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/zhiqi-wellness/frontend/dist;
        try_files \$uri \$uri/ /index.html;
    }

    # API代理
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/zhiqi-wellness /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 6. SSL证书配置 (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 📊 监控和维护

#### **应用监控**
```bash
# 健康检查
curl http://localhost:5000/api/health

# 性能监控
pip install gunicorn[gevent]
# 使用gevent worker提高并发性能

# 日志轮转
sudo tee /etc/logrotate.d/zhiqi-wellness > /dev/null <<EOF
/var/log/zhiqi-wellness/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 644 www-data www-data
    postrotate
        systemctl reload zhiqi-backend
    endscript
}
EOF
```

#### **数据库维护**
```bash
# 每日备份
crontab -e
# 添加: 0 2 * * * mysqldump wellness_platform_db > /backup/daily_$(date +\%Y\%m\%d).sql

# 性能监控
mysql -u root -p -e "SHOW PROCESSLIST;"
mysql -u root -p -e "SHOW ENGINE INNODB STATUS\G"

# 索引优化
mysql -u root -p wellness_platform_db -e "ANALYZE TABLE users, orders, activities;"
```

### 🔄 CI/CD流水线

#### **GitHub Actions配置**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest tests/ -v

      - name: Test Frontend
        run: |
          cd frontend
          npm ci
          npm run lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.PRODUCTION_HOST }}
          username: ${{ secrets.PRODUCTION_USER }}
          key: ${{ secrets.PRODUCTION_SSH_KEY }}
          script: |
            cd /var/www/zhiqi-wellness
            git pull origin main
            docker-compose down
            docker-compose build --no-cache
            docker-compose up -d
```

### 🔍 故障排除

#### **常见问题**
```bash
# 端口占用
sudo lsof -i :5000
sudo kill -9 <PID>

# 权限问题
sudo chown -R www-data:www-data /var/www/zhiqi-wellness
sudo chmod -R 755 /var/www/zhiqi-wellness

# 数据库连接失败
mysql -u zhiqi_user -p wellness_platform_db
# 检查用户权限和密码

# 内存不足
free -h
# 考虑增加交换空间或升级服务器配置
```

#### **日志分析**
```bash
# 查看应用日志
tail -f /var/log/zhiqi-wellness/app.log

# 查看Nginx错误日志
tail -f /var/log/nginx/error.log

# 查看系统日志
journalctl -u zhiqi-backend -f

# 数据库慢查询日志
mysql -u root -p -e "SHOW VARIABLES LIKE 'slow_query_log%';"
```

---

## 🤝 贡献指南

### 📝 开发规范

#### **代码风格**
```bash
# Python代码规范 (PEP 8)
pip install black flake8 isort
black backend/                    # 自动格式化
flake8 backend/                  # 代码检查
isort backend/                   # 导入排序

# JavaScript代码规范
cd frontend
npm run lint                     # ESLint检查
npm run lint-fix                # 自动修复
```

#### **提交规范**
```bash
# 提交消息格式
<type>(<scope>): <subject>

# 类型说明
feat:     新功能
fix:      修复bug
docs:     文档更新
style:    代码风格调整
refactor: 代码重构
test:     测试相关
chore:    构建工具配置

# 示例
feat(auth): 添加用户注册功能
fix(payment): 修复支付宝回调处理
docs(readme): 更新部署文档
```

#### **分支管理**
```bash
# 主分支
main        # 生产环境代码
develop     # 开发环境代码

# 功能分支命名
feature/user-auth           # 用户认证功能
feature/payment-integration # 支付集成功能
bugfix/login-validation     # 登录验证修复
hotfix/security-patch       # 安全补丁
```

### 🔄 开发工作流

#### **1. 环境准备**
```bash
# 克隆项目
git clone https://github.com/your-repo/zhiqi-wellness.git
cd zhiqi-wellness

# 创建开发分支
git checkout -b feature/your-feature-name

# 安装依赖
pip install -r backend/requirements.txt
cd frontend && npm install
```

#### **2. 开发过程**
```bash
# 启动开发环境
docker-compose up -d db          # 启动数据库
cd backend && python3 app.py     # 启动后端
cd frontend && npm run serve     # 启动前端

# 编写代码
# 添加测试
# 提交更改
```

#### **3. 代码提交**
```bash
# 添加文件到暂存区
git add .

# 提交更改
git commit -m "feat: 添加用户认证功能"

# 推送分支
git push origin feature/your-feature-name

# 创建Pull Request
```

### 🧪 测试要求

#### **后端测试**
```python
# 创建测试文件 backend/tests/test_feature.py
import unittest
from app import app, db

class TestFeature(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # 测试数据准备

    def test_feature_functionality(self):
        # 测试逻辑
        pass

if __name__ == '__main__':
    unittest.main()
```

#### **前端测试**
```javascript
// 创建测试文件 frontend/tests/unit/component.spec.js
import { shallowMount } from '@vue/test-utils'
import Component from '@/components/Component.vue'

describe('Component', () => {
  it('renders correctly', () => {
    const wrapper = shallowMount(Component)
    expect(wrapper.exists()).toBe(true)
  })
})
```

### 📋 Issue和PR规范

#### **Issue模板**
```markdown
## 问题描述
清晰简洁地描述问题

## 复现步骤
1. 进入页面 '...'
2. 点击按钮 '...'
3. 出现错误 '...'

## 期望结果
描述期望的行为

## 环境信息
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome 91]
- Version: [e.g. v1.0.0]
```

#### **PR模板**
```markdown
## 描述
简要描述这次PR做了什么

## 类型
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📚 Documentation
- [ ] 🎨 Code style

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 添加了相应的测试
- [ ] 更新了相关文档
- [ ] 在本地测试通过

## 关联Issue
Closes #123
```

### 🎯 项目进度

#### **✅ 已完成 (v1.0.0)**
- [x] **数据库架构设计** - 15个核心业务表，完整关系设计
- [x] **后端API开发** - 25+个RESTful接口，JWT认证
- [x] **前端应用框架** - Vue 3 + 路由 + 状态管理
- [x] **支付系统集成** - 微信支付 + 支付宝完整支持
- [x] **数据分析面板** - 销售分析 + 用户行为 + 收入统计
- [x] **品牌UI设计** - 灵芝主题 + 响应式设计
- [x] **部署运维** - Docker容器化 + CI/CD流水线
- [x] **安全特性** - 数据加密 + API安全 + 隐私保护

#### **🔄 进行中 (v1.1.0)**
- [ ] **AI智能推荐** - 基于用户行为的个性化推荐
- [ ] **多语言支持** - 国际化(i18n)功能
- [ ] **移动App** - React Native跨平台应用
- [ ] **高级分析** - 数据可视化大屏

#### **📋 规划中 (v2.0.0)**
- [ ] **微服务架构** - 服务拆分和容器化部署
- [ ] **区块链溯源** - 产品溯源上链
- [ ] **VR体验** - 虚拟现实养生体验
- [ ] **生态合作** - 第三方平台接入

---

## 📞 联系我们

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

## 📞 联系我们

- **官方网站**: [https://zhiqi-wellness.com](https://zhiqi-wellness.com)
- **技术支持**: support@zhiqi-wellness.com
- **商务合作**: business@zhiqi-wellness.com
- **地址**: 北京市朝阳区灵芝路88号

---

## 🎉 最新更新

### v1.0.0 - 完整商业化版本
- ✅ **支付系统**: 集成微信支付和支付宝，支持扫码支付
- ✅ **数据分析**: 完整的后台数据分析面板
- ✅ **支付页面**: 用户友好的支付流程和成功页面
- ✅ **单元测试**: 支付功能的完整测试覆盖
- ✅ **Docker部署**: 完整的容器化部署方案

---

<div align="center">

**芝栖养生平台** - 让健康成为一种生活方式 🌿💚

[![Star](https://img.shields.io/github/stars/zhiqi-wellness/platform.svg?style=social)](https://github.com/zhiqi-wellness/platform)
[![Fork](https://img.shields.io/github/forks/zhiqi-wellness/platform.svg?style=social)](https://github.com/zhiqi-wellness/platform)

</div>
