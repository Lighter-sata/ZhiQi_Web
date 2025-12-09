#!/bin/bash

# 芝栖养生平台 - 生产环境部署脚本
# 用于自动部署到Linux服务器

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 配置变量 (请根据实际情况修改)
APP_NAME="zhiqi-wellness"
DOMAIN="your-domain.com"
EMAIL="admin@your-domain.com"
DB_PASSWORD="secure_db_password"
JWT_SECRET="your-production-jwt-secret-key"
WECHAT_APP_ID="your_wechat_app_id"
WECHAT_MCH_ID="your_merchant_id"
ALIPAY_APP_ID="your_alipay_app_id"

# 服务器信息
SERVER_USER="root"
SERVER_HOST="your-server-ip"
SSH_KEY_PATH="$HOME/.ssh/id_rsa"

# 打印横幅
print_banner() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                  🚀 芝栖养生平台部署 🚀                     ║"
    echo "║                                                              ║"
    echo "║  🌐 域名: $DOMAIN                                          ║"
    echo "║  📧 邮箱: $EMAIL                                          ║"
    echo "║  🗄️ 数据库: MySQL 8.0                                      ║"
    echo "║  🐳 容器化: Docker + Nginx                                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

# 打印状态信息
print_step() {
    echo -e "${BLUE}📋 步骤 $1: $2${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${PURPLE}ℹ️  $1${NC}"
}

# 检查本地环境
check_local_env() {
    print_step "1" "检查本地环境"

    # 检查必需的命令
    local required_commands=("ssh" "scp" "git" "rsync")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            print_error "缺少必需命令: $cmd"
            exit 1
        fi
    done

    # 检查SSH密钥
    if [ ! -f "$SSH_KEY_PATH" ]; then
        print_error "SSH密钥不存在: $SSH_KEY_PATH"
        echo "请运行: ssh-keygen -t rsa -b 4096 -C \"$EMAIL\""
        exit 1
    fi

    print_success "本地环境检查通过"
}

# 服务器初始化
server_init() {
    print_step "2" "服务器环境初始化"

    echo "连接到服务器: $SERVER_USER@$SERVER_HOST"

    # 创建服务器初始化脚本
    cat > /tmp/server_init.sh << EOF
#!/bin/bash
set -e

echo "🔄 更新系统包..."
apt update && apt upgrade -y

echo "📦 安装基础工具..."
apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

echo "🐳 安装Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

echo "🐳 安装Docker Compose..."
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-\$(uname -s)-\$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "🔥 配置防火墙..."
ufw --force enable
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force reload

echo "👤 创建应用用户..."
useradd -m -s /bin/bash $APP_NAME || true
usermod -aG docker $APP_NAME

echo "📁 创建应用目录..."
mkdir -p /var/www/$APP_NAME
chown $APP_NAME:$APP_NAME /var/www/$APP_NAME

echo "✅ 服务器初始化完成"
EOF

    # 上传并执行初始化脚本
    scp -i "$SSH_KEY_PATH" /tmp/server_init.sh "$SERVER_USER@$SERVER_HOST:/tmp/"
    ssh -i "$SSH_KEY_PATH" "$SERVER_USER@$SERVER_HOST" "chmod +x /tmp/server_init.sh && /tmp/server_init.sh"

    print_success "服务器环境初始化完成"
}

# 上传代码
upload_code() {
    print_step "3" "上传应用代码"

    # 创建部署目录
    ssh -i "$SSH_KEY_PATH" "$SERVER_USER@$SERVER_HOST" "mkdir -p /var/www/$APP_NAME"

    # 上传代码 (排除不必要的文件)
    rsync -avz --exclude='.git/' \
               --exclude='__pycache__/' \
               --exclude='node_modules/' \
               --exclude='.env*' \
               --exclude='*.log' \
               --exclude='.DS_Store' \
               -e "ssh -i $SSH_KEY_PATH" \
               ./ "$SERVER_USER@$SERVER_HOST:/var/www/$APP_NAME/"

    print_success "应用代码上传完成"
}

# 配置环境变量
configure_env() {
    print_step "4" "配置环境变量"

    # 创建生产环境配置文件
    cat > /tmp/.env.production << EOF
# 生产环境配置 - 请根据实际情况修改

# Flask配置
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_PORT=5000

# 数据库配置
DATABASE_URL=mysql+mysqlconnector://zhiqi_user:$DB_PASSWORD@db:3306/wellness_platform_db

# JWT配置
JWT_SECRET_KEY=$JWT_SECRET
JWT_ACCESS_TOKEN_EXPIRES=24

# 支付配置
WECHAT_PAY_APP_ID=$WECHAT_APP_ID
WECHAT_PAY_MCH_ID=$WECHAT_MCH_ID
WECHAT_PAY_PRIVATE_KEY_PATH=/app/config/wechat_private_key.pem
WECHAT_PAY_SERIAL_NO=your_certificate_serial_no

ALIPAY_APP_ID=$ALIPAY_APP_ID
ALIPAY_PRIVATE_KEY=your_alipay_private_key
ALIPAY_PUBLIC_KEY=your_alipay_public_key
ALIPAY_NOTIFY_URL=https://$DOMAIN/api/payments/alipay/notify

# 文件上传配置
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=16777216

# 邮件配置 (可选)
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
SMTP_USERNAME=your_email@qq.com
SMTP_PASSWORD=your_smtp_password
FROM_EMAIL=noreply@$DOMAIN

# 监控配置 (可选)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
DATADOG_API_KEY=your-datadog-api-key

# CDN配置 (可选)
CDN_DOMAIN=https://cdn.your-domain.com
CDN_BUCKET=your-cdn-bucket

# 缓存配置 (可选)
REDIS_URL=redis://redis:6379/0
CACHE_TYPE=redis
CACHE_DEFAULT_TIMEOUT=300
EOF

    # 上传环境配置文件
    scp -i "$SSH_KEY_PATH" /tmp/.env.production "$SERVER_USER@$SERVER_HOST:/var/www/$APP_NAME/"

    print_success "环境变量配置完成"
}

# 部署应用
deploy_app() {
    print_step "5" "部署应用服务"

    # 创建部署脚本
    cat > /tmp/deploy_app.sh << EOF
#!/bin/bash
set -e

cd /var/www/$APP_NAME

echo "🐳 停止现有服务..."
docker-compose down || true

echo "🔧 构建新镜像..."
docker-compose build --no-cache

echo "🚀 启动服务..."
docker-compose up -d

echo "⏳ 等待服务启动..."
sleep 30

echo "🔍 检查服务状态..."
docker-compose ps

echo "🏥 检查健康状态..."
curl -f http://localhost:5000/api/health || echo "⚠️  后端服务可能未完全启动"

echo "✅ 应用部署完成"
EOF

    # 上传并执行部署脚本
    scp -i "$SSH_KEY_PATH" /tmp/deploy_app.sh "$SERVER_USER@$SERVER_HOST:/tmp/"
    ssh -i "$SSH_KEY_PATH" "$SERVER_USER@$SERVER_HOST" "chmod +x /tmp/deploy_app.sh && /tmp/deploy_app.sh"

    print_success "应用服务部署完成"
}

# 配置Nginx
configure_nginx() {
    print_step "6" "配置Nginx反向代理"

    # 创建Nginx配置文件
    cat > /tmp/nginx.conf << EOF
# 上游服务器
upstream backend {
    server localhost:5000;
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$host\$request_uri;
}

# HTTPS服务器
server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    # SSL证书 (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

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
    add_header Referrer-Policy "strict-origin-when-cross-origin";

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # API代理
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket支持 (如果需要)
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 前端应用
    location / {
        proxy_pass http://backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # SPA路由支持
        try_files \$uri \$uri/ /;

        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # 隐藏Nginx版本
    server_tokens off;
}

# 默认服务器
server {
    listen 80 default_server;
    listen 443 ssl default_server;
    server_name _;
    return 444;
}
EOF

    # 上传Nginx配置
    scp -i "$SSH_KEY_PATH" /tmp/nginx.conf "$SERVER_USER@$SERVER_HOST:/tmp/"

    # 配置Nginx
    ssh -i "$SSH_KEY_PATH" "$SERVER_USER@$SERVER_HOST" << EOF
# 备份现有配置
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup

# 复制新配置
cp /tmp/nginx.conf /etc/nginx/sites-available/$APP_NAME

# 启用站点
ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/

# 移除默认站点
rm -f /etc/nginx/sites-enabled/default

# 测试配置
nginx -t

# 重载Nginx
systemctl reload nginx

echo "✅ Nginx配置完成"
EOF

    print_success "Nginx反向代理配置完成"
}

# 配置SSL证书
configure_ssl() {
    print_step "7" "配置SSL证书"

    # 安装Certbot
    ssh -i "$SSH_KEY_PATH" "$SERVER_USER@$SERVER_HOST" << EOF
# 安装Certbot
apt install -y certbot python3-certbot-nginx

# 获取SSL证书
certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive

# 设置自动续期
(crontab -l ; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

# 重载Nginx
systemctl reload nginx

echo "✅ SSL证书配置完成"
EOF

    print_success "SSL证书配置完成"
}

# 配置监控
configure_monitoring() {
    print_step "8" "配置监控和日志"

    # 创建监控脚本
    cat > /tmp/monitoring.sh << EOF
#!/bin/bash

APP_NAME="$APP_NAME"
DOMAIN="$DOMAIN"
LOG_FILE="/var/log/\$APP_NAME/monitor.log"

# 创建日志目录
mkdir -p /var/log/\$APP_NAME

# 监控函数
check_services() {
    echo "\$(date): 检查服务状态" >> \$LOG_FILE

    # 检查Docker服务
    if docker-compose ps | grep -q "Up"; then
        echo "\$(date): ✅ Docker服务正常" >> \$LOG_FILE
    else
        echo "\$(date): ❌ Docker服务异常" >> \$LOG_FILE
        # 重启服务
        cd /var/www/\$APP_NAME && docker-compose restart
    fi

    # 检查Nginx
    if systemctl is-active --quiet nginx; then
        echo "\$(date): ✅ Nginx服务正常" >> \$LOG_FILE
    else
        echo "\$(date): ❌ Nginx服务异常" >> \$LOG_FILE
        systemctl restart nginx
    fi

    # 检查应用健康
    if curl -f -s http://localhost:5000/api/health > /dev/null; then
        echo "\$(date): ✅ 应用健康检查通过" >> \$LOG_FILE
    else
        echo "\$(date): ❌ 应用健康检查失败" >> \$LOG_FILE
    fi
}

# 磁盘使用监控
check_disk() {
    DISK_USAGE=\$(df / | tail -1 | awk '{print \$5}' | sed 's/%//')
    if [ "\$DISK_USAGE" -gt 90 ]; then
        echo "\$(date): ⚠️  磁盘使用率过高: \$DISK_USAGE%" >> \$LOG_FILE
        # 发送告警 (可以集成邮件或Webhook)
    fi
}

# 内存监控
check_memory() {
    MEM_USAGE=\$(free | grep Mem | awk '{printf "%.0f", \$3/\$2 * 100.0}')
    if [ "\$MEM_USAGE" -gt 85 ]; then
        echo "\$(date): ⚠️  内存使用率过高: \$MEM_USAGE%" >> \$LOG_FILE
    fi
}

# 执行监控
check_services
check_disk
check_memory

echo "\$(date): 监控完成" >> \$LOG_FILE
EOF

    # 上传监控脚本
    scp -i "$SSH_KEY_PATH" /tmp/monitoring.sh "$SERVER_USER@$SERVER_HOST:/tmp/"

    # 配置定时任务
    ssh -i "$SSH_KEY_PATH" "$SERVER_USER@$SERVER_HOST" << EOF
# 安装监控脚本
cp /tmp/monitoring.sh /usr/local/bin/\$APP_NAME-monitor.sh
chmod +x /usr/local/bin/\$APP_NAME-monitor.sh

# 添加定时任务 (每5分钟执行一次)
(crontab -l ; echo "*/5 * * * * /usr/local/bin/\$APP_NAME-monitor.sh") | crontab -

# 创建日志轮转
cat > /etc/logrotate.d/\$APP_NAME << EOF
/var/log/\$APP_NAME/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 644 root root
    postrotate
        systemctl reload \$APP_NAME 2>/dev/null || true
    endscript
}
EOF

echo "✅ 监控配置完成"
EOF

    print_success "监控和日志配置完成"
}

# 配置备份
configure_backup() {
    print_step "9" "配置数据备份"

    # 创建备份脚本
    cat > /tmp/backup.sh << EOF
#!/bin/bash

APP_NAME="$APP_NAME"
BACKUP_DIR="/var/backups/\$APP_NAME"
DATE=\$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# 创建备份目录
mkdir -p \$BACKUP_DIR

echo "\$(date): 开始备份..." >> \$BACKUP_DIR/backup.log

# 数据库备份
echo "备份数据库..."
docker exec \$(docker-compose ps -q db) mysqldump -u zhiqi_user -p$DB_PASSWORD wellness_platform_db > \$BACKUP_DIR/db_\$DATE.sql

# 压缩备份
echo "压缩备份文件..."
tar -czf \$BACKUP_DIR/backup_\$DATE.tar.gz -C \$BACKUP_DIR db_\$DATE.sql

# 加密备份 (可选)
# openssl enc -aes-256-cbc -salt -in \$BACKUP_DIR/backup_\$DATE.tar.gz -out \$BACKUP_DIR/backup_\$DATE.enc -k \$BACKUP_PASSWORD

# 删除临时文件
rm \$BACKUP_DIR/db_\$DATE.sql

# 删除过期备份
echo "清理过期备份..."
find \$BACKUP_DIR -name "backup_*.tar.gz" -mtime +\$RETENTION_DAYS -delete

# 上传到云存储 (可选)
# aws s3 cp \$BACKUP_DIR/backup_\$DATE.tar.gz s3://your-backup-bucket/

echo "\$(date): 备份完成" >> \$BACKUP_DIR/backup.log

# 发送通知 (可选)
# curl -X POST -H 'Content-type: application/json' --data '{"text":"数据库备份完成"}' \$SLACK_WEBHOOK_URL
EOF

    # 上传备份脚本
    scp -i "$SSH_KEY_PATH" /tmp/backup.sh "$SERVER_USER@$SERVER_HOST:/tmp/"

    # 配置定时备份
    ssh -i "$SSH_KEY_PATH" "$SERVER_USER@$SERVER_HOST" << EOF
# 安装备份脚本
cp /tmp/backup.sh /usr/local/bin/\$APP_NAME-backup.sh
chmod +x /usr/local/bin/\$APP_NAME-backup.sh

# 添加定时备份任务 (每天凌晨2点)
(crontab -l ; echo "0 2 * * * /usr/local/bin/\$APP_NAME-backup.sh") | crontab -

echo "✅ 备份配置完成"
EOF

    print_success "数据备份配置完成"
}

# 最终检查
final_check() {
    print_step "10" "最终检查和验证"

    echo "🔍 验证部署结果..."

    # 检查服务状态
    ssh -i "$SSH_KEY_PATH" "$SERVER_USER@$SERVER_HOST" << EOF
echo "🐳 Docker服务状态:"
docker-compose ps

echo ""
echo "🌐 Nginx状态:"
systemctl status nginx --no-pager -l

echo ""
echo "🔒 SSL证书信息:"
certbot certificates

echo ""
echo "💾 磁盘使用情况:"
df -h /

echo ""
echo "🧠 内存使用情况:"
free -h
EOF

    # 测试应用访问
    echo ""
    echo "🌐 测试应用访问..."
    if curl -f -s "https://$DOMAIN/api/health" > /dev/null; then
        print_success "应用访问正常"
    else
        print_warning "应用访问异常，请检查服务状态"
    fi

    # 打印访问信息
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                     🎉 部署完成！🎉                          ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  🌐 网站地址: https://$DOMAIN                             ║"
    echo "║  📚 API文档: https://$DOMAIN (Swagger UI)                 ║"
    echo "║  👤 管理后台: https://$DOMAIN/admin                       ║"
    echo "║  📧 管理员邮箱: $EMAIL                                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📋 重要提醒:"
    echo "   1. 请及时修改默认密码和密钥"
    echo "   2. 配置支付参数 (微信支付、支付宝)"
    echo "   3. 设置邮件服务用于通知"
    echo "   4. 监控日志文件: /var/log/$APP_NAME/"
    echo "   5. 备份位置: /var/backups/$APP_NAME/"
    echo ""
}

# 清理临时文件
cleanup() {
    print_info "清理临时文件..."
    rm -f /tmp/server_init.sh /tmp/deploy_app.sh /tmp/nginx.conf /tmp/.env.production /tmp/monitoring.sh /tmp/backup.sh
    print_success "清理完成"
}

# 主函数
main() {
    # 检查参数
    if [ $# -eq 0 ]; then
        echo "用法: $0 [init|deploy|update]"
        echo ""
        echo "  init   - 初始化服务器环境"
        echo "  deploy - 完整部署应用"
        echo "  update - 更新应用代码"
        exit 1
    fi

    local command="$1"

    case "$command" in
        "init")
            print_banner
            check_local_env
            server_init
            ;;
        "deploy")
            print_banner
            check_local_env
            server_init
            upload_code
            configure_env
            deploy_app
            configure_nginx
            configure_ssl
            configure_monitoring
            configure_backup
            final_check
            cleanup
            ;;
        "update")
            print_banner
            check_local_env
            upload_code
            deploy_app
            final_check
            ;;
        *)
            print_error "未知命令: $command"
            echo "支持的命令: init, deploy, update"
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"