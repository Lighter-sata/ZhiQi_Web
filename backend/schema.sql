-- 创建数据库 (如果不存在)
CREATE DATABASE IF NOT EXISTS wellness_platform_db;
USE wellness_platform_db;

-- 用户表 (扩展版)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    avatar VARCHAR(255),
    real_name VARCHAR(100),
    gender ENUM('male', 'female', 'other'),
    birth_date DATE,
    member_level ENUM('normal', 'vip', 'premium') DEFAULT 'normal',
    points INT DEFAULT 0,
    total_spent DECIMAL(10, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 内容表 (文章、视频、知识等)
CREATE TABLE IF NOT EXISTS content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content_type ENUM('article', 'video', 'knowledge', 'vlog') NOT NULL,
    summary TEXT,
    content TEXT,
    author_id INT,
    category VARCHAR(100),
    tags JSON,
    cover_image VARCHAR(255),
    video_url VARCHAR(255),
    reading_time INT, -- 分钟
    views_count INT DEFAULT 0,
    likes_count INT DEFAULT 0,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    publish_time TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 产品表
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category ENUM('lingzhi', 'tea', 'spore', 'gift', 'subscription') NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    original_price DECIMAL(10, 2),
    stock_quantity INT DEFAULT 0,
    sku VARCHAR(100) UNIQUE,
    images JSON, -- 产品图片数组
    specifications JSON, -- 产品规格
    trace_code VARCHAR(255), -- 溯源二维码
    is_featured BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    weight DECIMAL(5, 2), -- 重量(kg)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 活动表
CREATE TABLE IF NOT EXISTS activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    activity_type ENUM('workshop', 'experience', 'course', 'event') NOT NULL,
    category VARCHAR(100), -- 瑜伽、手作、采摘等
    organizer_id INT,
    organizer_type ENUM('official', 'host', 'user') DEFAULT 'official',
    max_participants INT,
    current_participants INT DEFAULT 0,
    price DECIMAL(10, 2) DEFAULT 0.00,
    location VARCHAR(255),
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    duration INT, -- 分钟
    images JSON,
    requirements TEXT, -- 参与要求
    platform_fee_rate DECIMAL(3, 2) DEFAULT 0.10, -- 平台服务费率 10%
    status ENUM('draft', 'pending_review', 'published', 'ongoing', 'completed', 'cancelled') DEFAULT 'draft',
    review_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    review_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 实体体验基地表
CREATE TABLE IF NOT EXISTS experience_bases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    province VARCHAR(100),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(255),
    images JSON,
    facilities JSON, -- 设施描述
    features JSON, -- 特色功能区
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 基地套餐表
CREATE TABLE IF NOT EXISTS base_packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    base_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    type ENUM('night_stay', 'weekend_workshop', 'custom') NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    duration_hours INT, -- 时长
    includes JSON, -- 包含内容
    max_capacity INT,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (base_id) REFERENCES experience_bases(id) ON DELETE CASCADE
);

-- 统一订单表
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    order_type ENUM('product', 'activity', 'accommodation', 'subscription') NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    platform_fee DECIMAL(10, 2) DEFAULT 0.00,
    payment_method ENUM('wechat', 'alipay', 'card') DEFAULT 'wechat',
    payment_status ENUM('pending', 'paid', 'refunded', 'failed') DEFAULT 'pending',
    order_status ENUM('pending', 'confirmed', 'processing', 'shipped', 'completed', 'cancelled') DEFAULT 'pending',
    shipping_address JSON,
    contact_info JSON,
    notes TEXT,
    paid_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 订单明细表
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_type ENUM('product', 'activity', 'package') NOT NULL,
    item_id INT NOT NULL, -- 对应的产品/活动/套餐ID
    quantity INT DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    item_snapshot JSON, -- 快照数据，避免历史数据变化
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- 支付记录表
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method ENUM('wechat', 'alipay', 'card') NOT NULL,
    transaction_id VARCHAR(255) UNIQUE,
    amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('pending', 'success', 'failed', 'refunded') DEFAULT 'pending',
    payment_data JSON, -- 支付网关返回数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- 评论表 (通用评论系统)
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    target_type ENUM('product', 'activity', 'content', 'base') NOT NULL,
    target_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    comment TEXT,
    images JSON,
    is_anonymous BOOLEAN DEFAULT FALSE,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'approved',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 收藏表
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    target_type ENUM('product', 'activity', 'content') NOT NULL,
    target_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_favorite (user_id, target_type, target_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 消息通知表
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    notification_type ENUM('system', 'order', 'activity', 'promotion') DEFAULT 'system',
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 用户活动参与记录表
CREATE TABLE IF NOT EXISTS user_activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_id INT NOT NULL,
    order_id INT,
    participation_status ENUM('registered', 'attended', 'cancelled', 'no_show') DEFAULT 'registered',
    check_in_time TIMESTAMP NULL,
    feedback_rating INT,
    feedback_comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL
);

-- 管理日志表
CREATE TABLE IF NOT EXISTS admin_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT,
    action VARCHAR(255) NOT NULL,
    target_type VARCHAR(100),
    target_id INT,
    details JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 创建索引以提高查询性能
CREATE INDEX idx_content_type ON content(content_type, status);
CREATE INDEX idx_content_publish_time ON content(publish_time);
CREATE INDEX idx_products_category ON products(category, is_available);
CREATE INDEX idx_activities_type ON activities(activity_type, status, start_time);
CREATE INDEX idx_activities_organizer ON activities(organizer_id, organizer_type);
CREATE INDEX idx_orders_user ON orders(user_id, created_at);
CREATE INDEX idx_orders_status ON orders(order_status, payment_status);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_reviews_target ON reviews(target_type, target_id, status);
CREATE INDEX idx_user_activities_user ON user_activities(user_id, participation_status);
