# ==========================================
# 芝栖养生平台 - 多阶段Docker构建
# ==========================================

# 第一阶段：构建前端静态文件
FROM node:16-alpine AS frontend-builder

WORKDIR /app/frontend

# 复制package文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY frontend/ .

# 构建生产版本
RUN npm run build

# ==========================================
# 第二阶段：Python环境准备
# ==========================================

FROM python:3.9-slim AS python-base

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# ==========================================
# 第三阶段：生产环境
# ==========================================

FROM python-base AS production

# 设置工作目录
WORKDIR /app

# 复制后端代码
COPY backend/ ./backend/
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 从前端构建阶段复制静态文件
COPY --from=frontend-builder /app/frontend/dist ./static

# 创建上传目录
RUN mkdir -p uploads && \
    chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "backend.app:app"]
