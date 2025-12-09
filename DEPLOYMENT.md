# 🚀 芝栖养生平台 - 服务器部署指南

## 📋 目录

- [服务器要求](#服务器要求)
- [部署前准备](#部署前准备)
- [一键部署](#一键部署)
- [手动部署](#手动部署)
- [域名配置](#域名配置)
- [SSL证书](#ssl证书)
- [数据库配置](#数据库配置)
- [支付配置](#支付配置)
- [监控维护](#监控维护)
- [故障排除](#故障排除)

---

## 🖥️ 服务器要求

### 最低配置
- **CPU**: 1核
- **内存**: 2GB RAM
- **存储**: 20GB SSD
- **网络**: 1Mbps 带宽
- **操作系统**: Ubuntu 20.04+ / CentOS 8+

### 推荐配置
- **CPU**: 2核+
- **内存**: 4GB RAM+
- **存储**: 50GB SSD+
- **网络**: 3Mbps+ 带宽
- **操作系统**: Ubuntu 22.04 LTS

### 网络要求
- 服务器必须有公网IP
- 开放端口: 22(SSH), 80(HTTP), 443(HTTPS)
- 域名已解析到服务器IP

---

## 🔧 部署前准备

### 1. 本地环境准备

```bash
# 确保本地有以下工具
which ssh scp rsync git curl wget
# 如果缺少，请安装: apt install openssh-client git curl wget rsync

# 生成SSH密钥 (如果没有)
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

### 2. 服务器采购和初始化

```bash
# 推荐服务商: 阿里云、腾讯云、AWS EC2、DigitalOcean

# 服务器购买建议:
# - 地域: 选择用户最近的地域
# - 操作系统: Ubuntu 22.04 LTS
# - 安全组: 只开放必要端口 (22, 80, 443)
```

### 3. 修改部署配置

编辑 `deploy.sh` 文件中的配置变量:

```bash
# 应用配置
APP_NAME="zhiqi-wellness"           # 应用名称
DOMAIN="your-domain.com"             # 域名
EMAIL="admin@your-domain.com"        # 管理员邮箱

# 数据库配置
DB_PASSWORD="secure_db_password"     # 数据库密码

# 安全配置
JWT_SECRET="your-production-jwt-secret-key"  # JWT密钥

# 支付配置 (生产环境需要)
WECHAT_APP_ID="your_wechat_app_id"
WECHAT_MCH_ID="your_merchant_id"
ALIPAY_APP_ID="your_alipay_app_id"

# 服务器连接信息
SERVER_USER="root"                   # 服务器用户名
SERVER_HOST="your-server-ip"         # 服务器IP
SSH_KEY_PATH="$HOME/.ssh/id_rsa"     # SSH密钥路径
```

### 4. 域名解析

```bash
# 在域名服务商处添加A记录
# 类型: A
# 主机记录: @ (或 www)
# 记录值: 你的服务器IP地址

# 示例:
# your-domain.com    A    123.456.789.012
# www.your-domain.com A   123.456.789.012
```

---

## 🚀 一键部署

### 方式一：完整部署 (推荐新服务器)

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/zhiqi-wellness.git
cd zhiqi-wellness

# 2. 修改配置 (编辑deploy.sh中的变量)

# 3. 执行一键部署
chmod +x deploy.sh
./deploy.sh deploy
```

### 方式二：仅初始化服务器

```bash
# 只初始化服务器环境，不部署应用
./deploy.sh init
```

### 方式三：更新现有部署

```bash
# 更新代码和重启服务
./deploy.sh update
```

### 部署过程说明

一键部署脚本会自动执行以下步骤:

1. **环境检查** - 验证本地环境和服务器连接
2. **服务器初始化** - 安装Docker、配置防火墙、创建用户
3. **代码上传** - 上传应用代码到服务器
4. **环境配置** - 生成生产环境配置文件
5. **服务部署** - 构建和启动Docker容器
6. **Nginx配置** - 配置反向代理和静态文件服务
7. **SSL证书** - 自动申请Let's Encrypt证书
8. **监控配置** - 设置日志轮转和健康检查
9. **备份配置** - 配置自动数据库备份
10. **最终验证** - 检查部署结果和应用访问

---

## 🔨 手动部署

如果需要更精细的控制，可以手动执行部署步骤。

### 1. 服务器环境准备

```bash
# 连接到服务器
ssh root@your-server-ip

# 更新系统
apt update && apt upgrade -y

# 安装必要工具
apt install -y curl wget git unzip ufw

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 配置防火墙
ufw --force enable
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force reload

# 创建应用用户
useradd -m -s /bin/bash zhiqi-wellness
usermod -aG docker zhiqi-wellness

# 创建应用目录
mkdir -p /var/www/zhiqi-wellness
chown zhiqi-wellness:zhiqi-wellness /var/www/zhiqi-wellness
```

### 2. 上传代码

```bash
# 在本地执行
rsync -avz --exclude='.git/' \
           --exclude='__pycache__/' \
           --exclude='node_modules/' \
           ./ root@your-server-ip:/var/www/zhiqi-wellness/
```

### 3. 配置环境变量

```bash
# 在服务器上创建环境文件
nano /var/www/zhiqi-wellness/.env.production
```

添加以下内容:

```bash
# Flask配置
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_PORT=5000

# 数据库配置
DATABASE_URL=mysql+mysqlconnector://zhiqi_user:your_db_password@db:3306/wellness_platform_db

# JWT配置
JWT_SECRET_KEY=your-production-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=24

# 支付配置
WECHAT_PAY_APP_ID=your_wechat_app_id
WECHAT_PAY_MCH_ID=your_merchant_id
WECHAT_PAY_PRIVATE_KEY_PATH=/app/config/wechat_private_key.pem
WECHAT_PAY_SERIAL_NO=your_certificate_serial_no

ALIPAY_APP_ID=your_alipay_app_id
ALIPAY_PRIVATE_KEY=your_alipay_private_key
ALIPAY_PUBLIC_KEY=your_alipay_public_key
ALIPAY_NOTIFY_URL=https://your-domain.com/api/payments/alipay/notify

# 文件上传配置
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=16777216

# 邮件配置 (可选)
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
SMTP_USERNAME=your_email@qq.com
SMTP_PASSWORD=your_smtp_password
FROM_EMAIL=noreply@your-domain.com
```

### 4. 部署应用

```bash
# 进入应用目录
cd /var/www/zhiqi-wellness

# 构建并启动服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 5. 配置Nginx

```bash
# 安装Nginx
apt install -y nginx

# 创建站点配置
nano /etc/nginx/sites-available/zhiqi-wellness
```

添加以下内容:

```nginx
# 上游服务器
upstream backend {
    server localhost:5000;
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$host$request_uri;
}

# HTTPS服务器
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL证书路径 (稍后配置)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 安全头
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # API代理
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 前端应用
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

启用站点配置:

```bash
# 启用站点
ln -s /etc/nginx/sites-available/zhiqi-wellness /etc/nginx/sites-enabled/

# 删除默认站点
rm /etc/nginx/sites-enabled/default

# 测试配置
nginx -t

# 重载Nginx
systemctl reload nginx
```

---

## 🌐 域名配置

### 1. DNS解析

在域名服务商处添加DNS记录:

```
类型: A
主机记录: @
记录值: 你的服务器IP

类型: A
主机记录: www
记录值: 你的服务器IP
```

### 2. 验证解析

```bash
# 检查DNS解析
nslookup your-domain.com

# 或使用dig
dig your-domain.com

# 等待DNS生效 (可能需要几分钟到24小时)
```

### 3. Nginx域名配置

确保Nginx配置中的 `server_name` 包含你的域名:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    # ... 其他配置
}
```

---

## 🔒 SSL证书

### 自动申请 (推荐)

```bash
# 安装Certbot
apt install -y certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your-domain.com -d www.your-domain.com

# 设置自动续期
(crontab -l ; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
```

### 手动配置

如果使用其他SSL证书:

```bash
# 将证书文件放到正确位置
cp your-domain.crt /etc/ssl/certs/
cp your-domain.key /etc/ssl/private/

# 修改Nginx配置
ssl_certificate /etc/ssl/certs/your-domain.crt;
ssl_certificate_key /etc/ssl/private/your-domain.key;

# 重载Nginx
nginx -t && nginx -s reload
```

### SSL测试

```bash
# 测试SSL配置
curl -I https://your-domain.com

# SSL证书信息
openssl s_client -connect your-domain.com:443 -servername your-domain.com < /dev/null | openssl x509 -noout -dates -subject
```

---

## 🗄️ 数据库配置

### Docker环境数据库

```bash
# 进入数据库容器
docker-compose exec db mysql -u zhiqi_user -p wellness_platform_db

# 默认密码: zhiqi_password (请修改)
```

### 生产环境数据库

```bash
# 连接MySQL
mysql -u zhiqi_user -p wellness_platform_db

# 创建应用用户
CREATE USER 'zhiqi_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON wellness_platform_db.* TO 'zhiqi_user'@'localhost';
FLUSH PRIVILEGES;

# 导入表结构
source /var/www/zhiqi-wellness/backend/schema.sql;
```

### 数据库优化

```sql
-- 生产环境推荐配置
SET GLOBAL innodb_buffer_pool_size = 1073741824; -- 1GB (根据内存调整)
SET GLOBAL innodb_log_file_size = 268435456;     -- 256MB
SET GLOBAL max_connections = 200;

-- 启用慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
```

---

## 💳 支付配置

### 微信支付配置

1. **申请微信支付商户号**
   - 访问: https://pay.weixin.qq.com
   - 完成商户入驻

2. **获取配置信息**
   - AppID
   - 商户号(MchId)
   - API密钥
   - 证书序列号

3. **配置服务器**
   ```bash
   # 将私钥文件放到服务器
   scp wechat_private_key.pem root@server:/var/www/zhiqi-wellness/config/

   # 更新环境变量
   WECHAT_PAY_APP_ID="your_app_id"
   WECHAT_PAY_MCH_ID="your_merchant_id"
   WECHAT_PAY_PRIVATE_KEY_PATH="/app/config/wechat_private_key.pem"
   WECHAT_PAY_SERIAL_NO="your_certificate_serial_no"
   ```

### 支付宝配置

1. **申请支付宝应用**
   - 访问: https://open.alipay.com
   - 创建应用并签约支付功能

2. **获取配置信息**
   - AppID
   - 应用私钥
   - 支付宝公钥

3. **配置服务器**
   ```bash
   # 更新环境变量
   ALIPAY_APP_ID="your_app_id"
   ALIPAY_PRIVATE_KEY="your_private_key_string"
   ALIPAY_PUBLIC_KEY="your_public_key_string"
   ALIPAY_NOTIFY_URL="https://your-domain.com/api/payments/alipay/notify"
   ```

### 支付测试

```bash
# 测试支付功能
curl -X POST http://localhost:5000/api/payments/create-payment \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "payment_method": "wechat"
  }'
```

---

## 📊 监控维护

### 日志查看

```bash
# Docker日志
docker-compose logs -f backend
docker-compose logs -f frontend

# Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# 应用日志
tail -f /var/log/zhiqi-wellness/app.log
```

### 性能监控

```bash
# 系统资源
htop
df -h
free -h
iostat -x 1

# Docker资源
docker stats

# 网络连接
netstat -tlnp
ss -tlnp
```

### 备份恢复

```bash
# 手动备份
docker-compose exec db mysqldump -u zhiqi_user -p wellness_platform_db > backup_$(date +%Y%m%d).sql

# 恢复备份
docker-compose exec -T db mysql -u zhiqi_user -p wellness_platform_db < backup_20231201.sql
```

### 更新部署

```bash
# 拉取最新代码
git pull origin main

# 重建服务
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 数据库迁移 (如果需要)
docker-compose exec backend flask db upgrade
```

---

## 🔧 故障排除

### 常见问题

#### 1. 服务无法启动

```bash
# 检查Docker服务
docker-compose ps

# 查看详细日志
docker-compose logs backend

# 检查端口占用
netstat -tlnp | grep :5000

# 重启服务
docker-compose restart backend
```

#### 2. 数据库连接失败

```bash
# 检查数据库服务
docker-compose exec db mysqladmin ping

# 检查数据库用户权限
docker-compose exec db mysql -u zhiqi_user -p -e "SHOW GRANTS;"

# 重置数据库密码
docker-compose exec db mysql -u root -p -e "ALTER USER 'zhiqi_user'@'%' IDENTIFIED BY 'new_password';"
```

#### 3. Nginx配置错误

```bash
# 测试配置
nginx -t

# 查看错误日志
tail -f /var/log/nginx/error.log

# 重载配置
nginx -s reload
```

#### 4. SSL证书问题

```bash
# 检查证书状态
certbot certificates

# 续期证书
certbot renew

# 强制HTTPS
# 确保Nginx配置中没有HTTP到HTTPS的重定向问题
```

#### 5. 支付功能异常

```bash
# 检查支付配置
docker-compose exec backend env | grep PAY

# 查看支付日志
docker-compose logs backend | grep payment

# 测试支付接口
curl -X POST http://localhost:5000/api/payments/create-payment \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "payment_method": "wechat"}'
```

### 紧急恢复

#### 快速重启所有服务
```bash
cd /var/www/zhiqi-wellness
docker-compose down
docker-compose up -d
```

#### 从备份恢复
```bash
# 停止服务
docker-compose down

# 恢复数据库
docker-compose exec -T db mysql -u zhiqi_user -p wellness_platform_db < backup.sql

# 重启服务
docker-compose up -d
```

#### 回滚部署
```bash
# 查看历史版本
git log --oneline -10

# 回滚到指定版本
git checkout <commit-hash>

# 重新部署
docker-compose build --no-cache
docker-compose up -d
```

---

## 📞 技术支持

### 联系方式
- **技术支持**: support@zhiqi-wellness.com
- **紧急联系**: emergency@zhiqi-wellness.com
- **项目主页**: https://github.com/zhiqi-wellness/platform

### 文档资源
- [API文档](https://your-domain.com/) - Swagger UI
- [用户手册](https://docs.zhiqi-wellness.com)
- [开发者文档](https://dev.zhiqi-wellness.com)

---

**🎉 恭喜！芝栖养生平台已成功部署到生产环境！**

请访问 `https://your-domain.com` 查看您的应用。

**重要提醒**:
1. 及时修改默认密码和安全密钥
2. 配置支付参数启用支付功能
3. 设置监控告警确保服务稳定
4. 定期备份数据保护重要信息
5. 关注服务器资源使用情况