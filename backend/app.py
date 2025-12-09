import os
import json
from datetime import datetime, timedelta
from decimal import Decimal
from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask_restx import Api, Resource, fields
import random
import string

app = Flask(__name__)

# MySQL 数据库配置 - 更新为养生平台数据库
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+mysqlconnector://your_mysql_user:your_mysql_password@localhost/wellness_platform_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'wellness-platform-secret-key-2024')  # 生产环境中请使用更安全的密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # Token有效期延长到24小时

# 文件上传配置
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 最大文件大小
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

jwt = JWTManager(app)
db = SQLAlchemy(app)

# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 用户表模型 (扩展版)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255))
    real_name = db.Column(db.String(100))
    gender = db.Column(db.Enum('male', 'female', 'other'))
    birth_date = db.Column(db.Date)
    member_level = db.Column(db.Enum('normal', 'vip', 'premium'), default='normal')
    points = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Numeric(10, 2), default=0.00)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    contents = db.relationship('Content', backref='author', lazy=True)
    activities = db.relationship('Activity', backref='organizer', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    user_activities = db.relationship('UserActivity', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'real_name': self.real_name,
            'gender': self.gender,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'member_level': self.member_level,
            'points': self.points,
            'total_spent': float(self.total_spent),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# 内容表模型
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.Enum('article', 'video', 'knowledge', 'vlog'), nullable=False)
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(100))
    tags = db.Column(db.JSON)
    cover_image = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    reading_time = db.Column(db.Integer)
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum('draft', 'published', 'archived'), default='draft')
    publish_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reviews = db.relationship('Review', backref='content', lazy=True, foreign_keys='Review.target_id')
    favorites = db.relationship('Favorite', backref='content', lazy=True, foreign_keys='Favorite.target_id')

    def __repr__(self):
        return f'<Content {self.title}>'

# 产品表模型
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.Enum('lingzhi', 'tea', 'spore', 'gift', 'subscription'), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    original_price = db.Column(db.Numeric(10, 2))
    stock_quantity = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(100), unique=True)
    images = db.Column(db.JSON)
    specifications = db.Column(db.JSON)
    trace_code = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    weight = db.Column(db.Numeric(5, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reviews = db.relationship('Review', backref='product', lazy=True, foreign_keys='Review.target_id')

    def __repr__(self):
        return f'<Product {self.name}>'

# 活动表模型
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    activity_type = db.Column(db.Enum('workshop', 'experience', 'course', 'event'), nullable=False)
    category = db.Column(db.String(100))
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    organizer_type = db.Column(db.Enum('official', 'host', 'user'), default='official')
    max_participants = db.Column(db.Integer)
    current_participants = db.Column(db.Integer, default=0)
    price = db.Column(db.Numeric(10, 2), default=0.00)
    location = db.Column(db.String(255))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer)
    images = db.Column(db.JSON)
    requirements = db.Column(db.Text)
    platform_fee_rate = db.Column(db.Numeric(3, 2), default=0.10)
    status = db.Column(db.Enum('draft', 'pending_review', 'published', 'ongoing', 'completed', 'cancelled'), default='draft')
    review_status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    review_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_activities = db.relationship('UserActivity', backref='activity', lazy=True)
    reviews = db.relationship('Review', backref='activity', lazy=True, foreign_keys='Review.target_id')

    def __repr__(self):
        return f'<Activity {self.title}>'

# 实体体验基地表模型
class ExperienceBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(255))
    images = db.Column(db.JSON)
    facilities = db.Column(db.JSON)
    features = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    packages = db.relationship('BasePackage', backref='base', lazy=True)

    def __repr__(self):
        return f'<ExperienceBase {self.name}>'

# 基地套餐表模型
class BasePackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('experience_base.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('night_stay', 'weekend_workshop', 'custom'), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    duration_hours = db.Column(db.Integer)
    includes = db.Column(db.JSON)
    max_capacity = db.Column(db.Integer)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BasePackage {self.name}>'

# 统一订单表模型
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_type = db.Column(db.Enum('product', 'activity', 'accommodation', 'subscription'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    platform_fee = db.Column(db.Numeric(10, 2), default=0.00)
    payment_method = db.Column(db.Enum('wechat', 'alipay', 'card'), default='wechat')
    payment_status = db.Column(db.Enum('pending', 'paid', 'refunded', 'failed'), default='pending')
    order_status = db.Column(db.Enum('pending', 'confirmed', 'processing', 'shipped', 'completed', 'cancelled'), default='pending')
    shipping_address = db.Column(db.JSON)
    contact_info = db.Column(db.JSON)
    notes = db.Column(db.Text)
    paid_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True)
    payments = db.relationship('Payment', backref='order', lazy=True)
    user_activities = db.relationship('UserActivity', backref='order', lazy=True, foreign_keys='UserActivity.order_id')

    def __repr__(self):
        return f'<Order {self.order_number}>'

# 订单明细表模型
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_type = db.Column(db.Enum('product', 'activity', 'package'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    item_snapshot = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<OrderItem {self.id}>'

# 支付记录表模型
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_method = db.Column(db.Enum('wechat', 'alipay', 'card'), nullable=False)
    transaction_id = db.Column(db.String(255), unique=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'success', 'failed', 'refunded'), default='pending')
    payment_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.transaction_id}>'

# 评论表模型 (通用评论系统)
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_type = db.Column(db.Enum('product', 'activity', 'content', 'base'), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255))
    comment = db.Column(db.Text)
    images = db.Column(db.JSON)
    is_anonymous = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='approved')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.id}>'

# 收藏表模型
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_type = db.Column(db.Enum('product', 'activity', 'content'), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'target_type', 'target_id', name='unique_favorite'),)

    def __repr__(self):
        return f'<Favorite {self.id}>'

# 消息通知表模型
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    notification_type = db.Column(db.Enum('system', 'order', 'activity', 'promotion'), default='system')
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.title}>'

# 用户活动参与记录表模型
class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    participation_status = db.Column(db.Enum('registered', 'attended', 'cancelled', 'no_show'), default='registered')
    check_in_time = db.Column(db.DateTime)
    feedback_rating = db.Column(db.Integer)
    feedback_comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserActivity {self.id}>'

# 管理日志表模型
class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(255), nullable=False)
    target_type = db.Column(db.String(100))
    target_id = db.Column(db.Integer)
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AdminLog {self.action}>'

api = Api(app, version='1.0', title='芝栖养生平台 API', description='综合养生健康平台API')

# 工具函数
def generate_order_number():
    """生成订单号"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f'WZ{timestamp}{random_str}'

def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 定义API模型 (用于Swagger文档)
# 用户相关模型
user_register_model = api.model('UserRegister', {
    'username': fields.String(required=True, description='用户名', min_length=3),
    'email': fields.String(required=True, description='邮箱地址'),
    'password': fields.String(required=True, description='密码', min_length=6),
    'phone': fields.String(description='手机号'),
    'real_name': fields.String(description='真实姓名')
})

user_login_model = api.model('UserLogin', {
    'username': fields.String(required=True, description='用户名'),
    'password': fields.String(required=True, description='密码')
})

user_profile_model = api.model('UserProfile', {
    'phone': fields.String(description='手机号'),
    'real_name': fields.String(description='真实姓名'),
    'gender': fields.String(enum=['male', 'female', 'other'], description='性别'),
    'birth_date': fields.Date(description='出生日期'),
    'avatar': fields.String(description='头像URL')
})

# 内容相关模型
content_model = api.model('Content', {
    'title': fields.String(required=True, description='标题'),
    'content_type': fields.String(required=True, enum=['article', 'video', 'knowledge', 'vlog'], description='内容类型'),
    'summary': fields.String(description='摘要'),
    'content': fields.String(description='内容'),
    'category': fields.String(description='分类'),
    'tags': fields.List(fields.String, description='标签'),
    'cover_image': fields.String(description='封面图片'),
    'video_url': fields.String(description='视频URL'),
    'reading_time': fields.Integer(description='阅读时间(分钟)'),
    'status': fields.String(enum=['draft', 'published', 'archived'], description='状态')
})

# 产品相关模型
product_model = api.model('Product', {
    'name': fields.String(required=True, description='产品名称'),
    'category': fields.String(required=True, enum=['lingzhi', 'tea', 'spore', 'gift', 'subscription'], description='产品分类'),
    'description': fields.String(description='产品描述'),
    'price': fields.Float(required=True, description='价格'),
    'original_price': fields.Float(description='原价'),
    'stock_quantity': fields.Integer(description='库存数量'),
    'sku': fields.String(description='SKU'),
    'images': fields.List(fields.String, description='产品图片'),
    'specifications': fields.Raw(description='产品规格'),
    'trace_code': fields.String(description='溯源码'),
    'is_featured': fields.Boolean(description='是否精选'),
    'weight': fields.Float(description='重量(kg)')
})

# 活动相关模型
activity_model = api.model('Activity', {
    'title': fields.String(required=True, description='活动标题'),
    'description': fields.String(description='活动描述'),
    'activity_type': fields.String(required=True, enum=['workshop', 'experience', 'course', 'event'], description='活动类型'),
    'category': fields.String(description='活动分类'),
    'max_participants': fields.Integer(description='最大参与人数'),
    'price': fields.Float(description='价格'),
    'location': fields.String(description='活动地点'),
    'start_time': fields.DateTime(required=True, description='开始时间'),
    'end_time': fields.DateTime(required=True, description='结束时间'),
    'duration': fields.Integer(description='持续时间(分钟)'),
    'images': fields.List(fields.String, description='活动图片'),
    'requirements': fields.String(description='参与要求')
})

# 订单相关模型
order_create_model = api.model('OrderCreate', {
    'order_type': fields.String(required=True, enum=['product', 'activity', 'accommodation', 'subscription'], description='订单类型'),
    'items': fields.List(fields.Raw, required=True, description='订单项'),
    'shipping_address': fields.Raw(description='收货地址'),
    'contact_info': fields.Raw(description='联系信息'),
    'notes': fields.String(description='备注')
})

# 评论相关模型
review_model = api.model('Review', {
    'target_type': fields.String(required=True, enum=['product', 'activity', 'content', 'base'], description='评论对象类型'),
    'target_id': fields.Integer(required=True, description='评论对象ID'),
    'rating': fields.Integer(required=True, min=1, max=5, description='评分(1-5)'),
    'title': fields.String(description='评论标题'),
    'comment': fields.String(description='评论内容'),
    'images': fields.List(fields.String, description='评论图片'),
    'is_anonymous': fields.Boolean(description='是否匿名')
})

@app.route('/')
def hello_world():
    return '芝栖养生平台 - Flask Backend!'

# 工具函数路由
@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """文件上传接口"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 返回文件URL
        file_url = f'/uploads/{filename}'
        return jsonify({'url': file_url, 'filename': filename}), 200

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """获取上传的文件"""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# 用户认证命名空间
auth_ns = api.namespace('auth', description='用户认证相关接口')

@auth_ns.route('/register')
class UserRegister(Resource):
    @auth_ns.expect(user_register_model)
    @auth_ns.response(201, '用户创建成功')
    @auth_ns.response(400, '缺少必要字段')
    @auth_ns.response(409, '用户名或邮箱已存在')
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        real_name = data.get('real_name')

        if not username or not password or not email:
            return jsonify({'msg': '缺少用户名、密码或邮箱'}), 400

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return jsonify({'msg': '用户名或邮箱已存在'}), 409

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password=hashed_password,
            email=email,
            phone=phone,
            real_name=real_name
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'msg': '用户创建成功', 'user_id': new_user.id}), 201

@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.expect(user_login_model)
    @auth_ns.response(200, '登录成功')
    @auth_ns.response(401, '用户名或密码错误')
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password) and user.is_active:
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'msg': '用户名或密码错误'}), 401

@auth_ns.route('/profile')
class UserProfile(Resource):
    @jwt_required()
    @auth_ns.response(200, '获取成功')
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'msg': '用户不存在'}), 404

        return jsonify({'user': user.to_dict()}), 200

    @jwt_required()
    @auth_ns.expect(user_profile_model)
    @auth_ns.response(200, '更新成功')
    def put(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'msg': '用户不存在'}), 404

        data = request.get_json()
        for field in ['phone', 'real_name', 'gender', 'birth_date', 'avatar']:
            if field in data:
                setattr(user, field, data[field])

        user.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'msg': '用户信息更新成功', 'user': user.to_dict()}), 200

# 内容管理命名空间
content_ns = api.namespace('content', description='内容管理相关接口')

@content_ns.route('/')
class ContentList(Resource):
    @content_ns.response(200, '获取成功')
    def get(self):
        """获取内容列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        content_type = request.args.get('type')
        category = request.args.get('category')
        status = request.args.get('status', 'published')

        query = Content.query

        if content_type:
            query = query.filter_by(content_type=content_type)
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)

        contents = query.order_by(Content.created_at.desc()).paginate(page=page, per_page=per_page)

        result = []
        for content in contents.items:
            result.append({
                'id': content.id,
                'title': content.title,
                'content_type': content.content_type,
                'summary': content.summary,
                'category': content.category,
                'tags': content.tags,
                'cover_image': content.cover_image,
                'views_count': content.views_count,
                'likes_count': content.likes_count,
                'status': content.status,
                'publish_time': content.publish_time.isoformat() if content.publish_time else None,
                'created_at': content.created_at.isoformat(),
                'author': {
                    'id': content.author.id,
                    'username': content.author.username,
                    'real_name': content.author.real_name
                } if content.author else None
            })

        return jsonify({
            'contents': result,
            'total': contents.total,
            'pages': contents.pages,
            'current_page': page
        }), 200

    @jwt_required()
    @content_ns.expect(content_model)
    @content_ns.response(201, '内容创建成功')
    def post(self):
        """创建内容"""
        current_user_id = get_jwt_identity()
        data = request.get_json()

        new_content = Content(
            title=data['title'],
            content_type=data['content_type'],
            summary=data.get('summary'),
            content=data.get('content'),
            author_id=current_user_id,
            category=data.get('category'),
            tags=data.get('tags', []),
            cover_image=data.get('cover_image'),
            video_url=data.get('video_url'),
            reading_time=data.get('reading_time'),
            status=data.get('status', 'draft')
        )

        db.session.add(new_content)
        db.session.commit()

        return jsonify({'msg': '内容创建成功', 'content_id': new_content.id}), 201

@content_ns.route('/<int:content_id>')
class ContentResource(Resource):
    @content_ns.response(200, '获取成功')
    @content_ns.response(404, '内容不存在')
    def get(self, content_id):
        """获取内容详情"""
        content = Content.query.get(content_id)
        if not content:
            return jsonify({'msg': '内容不存在'}), 404

        # 增加浏览量
        content.views_count += 1
        db.session.commit()

        return jsonify({
            'id': content.id,
            'title': content.title,
            'content_type': content.content_type,
            'summary': content.summary,
            'content': content.content,
            'category': content.category,
            'tags': content.tags,
            'cover_image': content.cover_image,
            'video_url': content.video_url,
            'reading_time': content.reading_time,
            'views_count': content.views_count,
            'likes_count': content.likes_count,
            'status': content.status,
            'publish_time': content.publish_time.isoformat() if content.publish_time else None,
            'created_at': content.created_at.isoformat(),
            'updated_at': content.updated_at.isoformat(),
            'author': {
                'id': content.author.id,
                'username': content.author.username,
                'real_name': content.author.real_name
            } if content.author else None
        }), 200

    @jwt_required()
    @content_ns.expect(content_model)
    @content_ns.response(200, '更新成功')
    @content_ns.response(403, '无权限')
    @content_ns.response(404, '内容不存在')
    def put(self, content_id):
        """更新内容"""
        current_user_id = get_jwt_identity()
        content = Content.query.get(content_id)

        if not content:
            return jsonify({'msg': '内容不存在'}), 404

        if content.author_id != current_user_id:
            return jsonify({'msg': '无权限修改此内容'}), 403

        data = request.get_json()
        for field in ['title', 'content_type', 'summary', 'content', 'category', 'tags',
                     'cover_image', 'video_url', 'reading_time', 'status']:
            if field in data:
                setattr(content, field, data[field])

        content.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'msg': '内容更新成功'}), 200

    @jwt_required()
    @content_ns.response(200, '删除成功')
    @content_ns.response(403, '无权限')
    @content_ns.response(404, '内容不存在')
    def delete(self, content_id):
        """删除内容"""
        current_user_id = get_jwt_identity()
        content = Content.query.get(content_id)

        if not content:
            return jsonify({'msg': '内容不存在'}), 404

        if content.author_id != current_user_id:
            return jsonify({'msg': '无权限删除此内容'}), 403

        db.session.delete(content)
        db.session.commit()

        return jsonify({'msg': '内容删除成功'}), 200

@content_ns.route('/<int:content_id>/like')
class ContentLike(Resource):
    @jwt_required()
    @content_ns.response(200, '操作成功')
    def post(self, content_id):
        """点赞/取消点赞内容"""
        current_user_id = get_jwt_identity()
        content = Content.query.get(content_id)

        if not content:
            return jsonify({'msg': '内容不存在'}), 404

        # 这里可以添加点赞记录逻辑
        content.likes_count += 1
        db.session.commit()

        return jsonify({'msg': '点赞成功', 'likes_count': content.likes_count}), 200

# 产品管理命名空间
product_ns = api.namespace('products', description='产品管理相关接口')

@product_ns.route('/')
class ProductList(Resource):
    @product_ns.response(200, '获取成功')
    def get(self):
        """获取产品列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category = request.args.get('category')
        is_featured = request.args.get('featured', type=bool)
        search = request.args.get('search')

        query = Product.query.filter_by(is_available=True)

        if category:
            query = query.filter_by(category=category)
        if is_featured:
            query = query.filter_by(is_featured=True)
        if search:
            query = query.filter(Product.name.contains(search) | Product.description.contains(search))

        products = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=per_page)

        result = []
        for product in products.items:
            result.append({
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'description': product.description,
                'price': float(product.price),
                'original_price': float(product.original_price) if product.original_price else None,
                'stock_quantity': product.stock_quantity,
                'images': product.images or [],
                'is_featured': product.is_featured,
                'trace_code': product.trace_code,
                'weight': float(product.weight) if product.weight else None,
                'created_at': product.created_at.isoformat()
            })

        return jsonify({
            'products': result,
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        }), 200

@product_ns.route('/<int:product_id>')
class ProductResource(Resource):
    @product_ns.response(200, '获取成功')
    @product_ns.response(404, '产品不存在')
    def get(self, product_id):
        """获取产品详情"""
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'msg': '产品不存在'}), 404

        return jsonify({
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'price': float(product.price),
            'original_price': float(product.original_price) if product.original_price else None,
            'stock_quantity': product.stock_quantity,
            'sku': product.sku,
            'images': product.images or [],
            'specifications': product.specifications or {},
            'trace_code': product.trace_code,
            'is_featured': product.is_featured,
            'is_available': product.is_available,
            'weight': float(product.weight) if product.weight else None,
            'created_at': product.created_at.isoformat(),
            'updated_at': product.updated_at.isoformat()
        }), 200

# 活动管理命名空间
activity_ns = api.namespace('activities', description='活动管理相关接口')

@activity_ns.route('/')
class ActivityList(Resource):
    @activity_ns.response(200, '获取成功')
    def get(self):
        """获取活动列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        activity_type = request.args.get('type')
        category = request.args.get('category')
        status = request.args.get('status', 'published')
        upcoming = request.args.get('upcoming', type=bool)

        query = Activity.query

        if activity_type:
            query = query.filter_by(activity_type=activity_type)
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        if upcoming:
            query = query.filter(Activity.start_time > datetime.utcnow())

        activities = query.order_by(Activity.start_time.asc()).paginate(page=page, per_page=per_page)

        result = []
        for activity in activities.items:
            result.append({
                'id': activity.id,
                'title': activity.title,
                'description': activity.description,
                'activity_type': activity.activity_type,
                'category': activity.category,
                'max_participants': activity.max_participants,
                'current_participants': activity.current_participants,
                'price': float(activity.price),
                'location': activity.location,
                'start_time': activity.start_time.isoformat(),
                'end_time': activity.end_time.isoformat(),
                'duration': activity.duration,
                'images': activity.images or [],
                'status': activity.status,
                'organizer': {
                    'id': activity.organizer.id,
                    'username': activity.organizer.username,
                    'real_name': activity.organizer.real_name,
                    'organizer_type': activity.organizer_type
                } if activity.organizer else None
            })

        return jsonify({
            'activities': result,
            'total': activities.total,
            'pages': activities.pages,
            'current_page': page
        }), 200

    @jwt_required()
    @activity_ns.expect(activity_model)
    @activity_ns.response(201, '活动创建成功')
    def post(self):
        """创建活动"""
        current_user_id = get_jwt_identity()
        data = request.get_json()

        new_activity = Activity(
            title=data['title'],
            description=data.get('description'),
            activity_type=data['activity_type'],
            category=data.get('category'),
            organizer_id=current_user_id,
            organizer_type=data.get('organizer_type', 'user'),
            max_participants=data.get('max_participants'),
            price=data.get('price', 0.00),
            location=data.get('location'),
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            duration=data.get('duration'),
            images=data.get('images', []),
            requirements=data.get('requirements'),
            status='pending_review' if data.get('organizer_type') == 'user' else 'draft'
        )

        db.session.add(new_activity)
        db.session.commit()

        return jsonify({'msg': '活动创建成功', 'activity_id': new_activity.id}), 201

@activity_ns.route('/<int:activity_id>')
class ActivityResource(Resource):
    @activity_ns.response(200, '获取成功')
    @activity_ns.response(404, '活动不存在')
    def get(self, activity_id):
        """获取活动详情"""
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'msg': '活动不存在'}), 404

        return jsonify({
            'id': activity.id,
            'title': activity.title,
            'description': activity.description,
            'activity_type': activity.activity_type,
            'category': activity.category,
            'max_participants': activity.max_participants,
            'current_participants': activity.current_participants,
            'price': float(activity.price),
            'location': activity.location,
            'start_time': activity.start_time.isoformat(),
            'end_time': activity.end_time.isoformat(),
            'duration': activity.duration,
            'images': activity.images or [],
            'requirements': activity.requirements,
            'platform_fee_rate': float(activity.platform_fee_rate),
            'status': activity.status,
            'review_status': activity.review_status,
            'review_reason': activity.review_reason,
            'created_at': activity.created_at.isoformat(),
            'updated_at': activity.updated_at.isoformat(),
            'organizer': {
                'id': activity.organizer.id,
                'username': activity.organizer.username,
                'real_name': activity.organizer.real_name,
                'organizer_type': activity.organizer_type
            } if activity.organizer else None
        }), 200

@activity_ns.route('/<int:activity_id>/register')
class ActivityRegistration(Resource):
    @jwt_required()
    @activity_ns.response(201, '报名成功')
    @activity_ns.response(400, '报名失败')
    @activity_ns.response(404, '活动不存在')
    def post(self, activity_id):
        """活动报名"""
        current_user_id = get_jwt_identity()
        activity = Activity.query.get(activity_id)

        if not activity:
            return jsonify({'msg': '活动不存在'}), 404

        if activity.status != 'published':
            return jsonify({'msg': '活动未发布，无法报名'}), 400

        if activity.current_participants >= activity.max_participants:
            return jsonify({'msg': '活动已满员'}), 400

        # 检查是否已经报名
        existing_registration = UserActivity.query.filter_by(
            user_id=current_user_id,
            activity_id=activity_id
        ).first()

        if existing_registration:
            return jsonify({'msg': '您已经报名此活动'}), 400

        # 创建报名记录
        registration = UserActivity(
            user_id=current_user_id,
            activity_id=activity_id,
            participation_status='registered'
        )

        activity.current_participants += 1

        db.session.add(registration)
        db.session.commit()

        return jsonify({'msg': '报名成功', 'registration_id': registration.id}), 201

# 实体体验基地命名空间
base_ns = api.namespace('bases', description='实体体验基地相关接口')

@base_ns.route('/')
class BaseList(Resource):
    @base_ns.response(200, '获取成功')
    def get(self):
        """获取基地列表"""
        bases = ExperienceBase.query.filter_by(is_active=True).all()

        result = []
        for base in bases:
            result.append({
                'id': base.id,
                'name': base.name,
                'description': base.description,
                'address': base.address,
                'city': base.city,
                'province': base.province,
                'contact_phone': base.contact_phone,
                'contact_email': base.contact_email,
                'images': base.images or [],
                'facilities': base.facilities or {},
                'features': base.features or {}
            })

        return jsonify({'bases': result}), 200

@base_ns.route('/<int:base_id>')
class BaseResource(Resource):
    @base_ns.response(200, '获取成功')
    @base_ns.response(404, '基地不存在')
    def get(self, base_id):
        """获取基地详情"""
        base = ExperienceBase.query.get(base_id)
        if not base:
            return jsonify({'msg': '基地不存在'}), 404

        packages = BasePackage.query.filter_by(base_id=base_id, is_available=True).all()
        packages_data = []
        for package in packages:
            packages_data.append({
                'id': package.id,
                'name': package.name,
                'type': package.type,
                'description': package.description,
                'price': float(package.price),
                'duration_hours': package.duration_hours,
                'includes': package.includes or [],
                'max_capacity': package.max_capacity
            })

        return jsonify({
            'id': base.id,
            'name': base.name,
            'description': base.description,
            'address': base.address,
            'city': base.city,
            'province': base.province,
            'contact_phone': base.contact_phone,
            'contact_email': base.contact_email,
            'images': base.images or [],
            'facilities': base.facilities or {},
            'features': base.features or {},
            'packages': packages_data,
            'created_at': base.created_at.isoformat(),
            'updated_at': base.updated_at.isoformat()
        }), 200

# 订单管理命名空间
order_ns = api.namespace('orders', description='订单管理相关接口')

@order_ns.route('/')
class OrderList(Resource):
    @jwt_required()
    @order_ns.response(200, '获取成功')
    def get(self):
        """获取用户订单列表"""
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        order_type = request.args.get('type')
        status = request.args.get('status')

        query = Order.query.filter_by(user_id=current_user_id)

        if order_type:
            query = query.filter_by(order_type=order_type)
        if status:
            query = query.filter_by(order_status=status)

        orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page)

        result = []
        for order in orders.items:
            items = []
            for item in order.items:
                items.append({
                    'id': item.id,
                    'item_type': item.item_type,
                    'item_id': item.item_id,
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price),
                    'total_price': float(item.total_price),
                    'item_snapshot': item.item_snapshot
                })

            result.append({
                'id': order.id,
                'order_number': order.order_number,
                'order_type': order.order_type,
                'total_amount': float(order.total_amount),
                'platform_fee': float(order.platform_fee),
                'payment_method': order.payment_method,
                'payment_status': order.payment_status,
                'order_status': order.order_status,
                'items': items,
                'created_at': order.created_at.isoformat(),
                'paid_at': order.paid_at.isoformat() if order.paid_at else None,
                'completed_at': order.completed_at.isoformat() if order.completed_at else None
            })

        return jsonify({
            'orders': result,
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page
        }), 200

    @jwt_required()
    @order_ns.expect(order_create_model)
    @order_ns.response(201, '订单创建成功')
    def post(self):
        """创建订单"""
        current_user_id = get_jwt_identity()
        data = request.get_json()

        order_type = data['order_type']
        items_data = data['items']

        # 计算订单总金额
        total_amount = 0.0
        platform_fee = 0.0
        order_items = []

        for item_data in items_data:
            if order_type == 'product':
                product = Product.query.get(item_data['product_id'])
                if not product or not product.is_available:
                    return jsonify({'msg': f'产品 {item_data["product_id"]} 不存在或已下架'}), 400

                quantity = item_data.get('quantity', 1)
                unit_price = float(product.price)
                total_price = unit_price * quantity

                order_items.append({
                    'item_type': 'product',
                    'item_id': product.id,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price,
                    'item_snapshot': {
                        'name': product.name,
                        'image': product.images[0] if product.images else None
                    }
                })

            elif order_type == 'activity':
                activity = Activity.query.get(item_data['activity_id'])
                if not activity or activity.status != 'published':
                    return jsonify({'msg': f'活动 {item_data["activity_id"]} 不存在或未发布'}), 400

                # 检查是否已经报名
                existing = UserActivity.query.filter_by(
                    user_id=current_user_id,
                    activity_id=activity.id
                ).first()
                if existing:
                    return jsonify({'msg': '您已经报名此活动'}), 400

                unit_price = float(activity.price)
                platform_fee_rate = float(activity.platform_fee_rate)
                platform_fee_item = unit_price * platform_fee_rate

                order_items.append({
                    'item_type': 'activity',
                    'item_id': activity.id,
                    'quantity': 1,
                    'unit_price': unit_price,
                    'total_price': unit_price,
                    'item_snapshot': {
                        'title': activity.title,
                        'start_time': activity.start_time.isoformat(),
                        'location': activity.location
                    }
                })

                platform_fee += platform_fee_item

            total_amount += order_items[-1]['total_price']

        # 创建订单
        order = Order(
            order_number=generate_order_number(),
            user_id=current_user_id,
            order_type=order_type,
            total_amount=total_amount,
            platform_fee=platform_fee,
            shipping_address=data.get('shipping_address'),
            contact_info=data.get('contact_info'),
            notes=data.get('notes')
        )

        db.session.add(order)
        db.session.flush()  # 获取订单ID

        # 添加订单项
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                item_type=item_data['item_type'],
                item_id=item_data['item_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                total_price=item_data['total_price'],
                item_snapshot=json.dumps(item_data['item_snapshot'])
            )
            db.session.add(order_item)

        db.session.commit()

        return jsonify({
            'msg': '订单创建成功',
            'order_id': order.id,
            'order_number': order.order_number,
            'total_amount': float(total_amount),
            'platform_fee': float(platform_fee)
        }), 201

# 评论管理命名空间
review_ns = api.namespace('reviews', description='评论管理相关接口')

@review_ns.route('/')
class ReviewList(Resource):
    @review_ns.response(200, '获取成功')
    def get(self):
        """获取评论列表"""
        target_type = request.args.get('target_type')
        target_id = request.args.get('target_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if not target_type or not target_id:
            return jsonify({'msg': '需要指定评论对象类型和ID'}), 400

        query = Review.query.filter_by(
            target_type=target_type,
            target_id=target_id,
            status='approved'
        )

        reviews = query.order_by(Review.created_at.desc()).paginate(page=page, per_page=per_page)

        result = []
        for review in reviews.items:
            result.append({
                'id': review.id,
                'user_id': review.user_id,
                'rating': review.rating,
                'title': review.title,
                'comment': review.comment,
                'images': review.images or [],
                'is_anonymous': review.is_anonymous,
                'created_at': review.created_at.isoformat(),
                'user': {
                    'username': review.user.username,
                    'real_name': review.user.real_name,
                    'avatar': review.user.avatar
                } if not review.is_anonymous else None
            })

        return jsonify({
            'reviews': result,
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page
        }), 200

    @jwt_required()
    @review_ns.expect(review_model)
    @review_ns.response(201, '评论提交成功')
    def post(self):
        """提交评论"""
        current_user_id = get_jwt_identity()
        data = request.get_json()

        # 检查是否已经评论过
        existing_review = Review.query.filter_by(
            user_id=current_user_id,
            target_type=data['target_type'],
            target_id=data['target_id']
        ).first()

        if existing_review:
            return jsonify({'msg': '您已经评论过此内容'}), 400

        review = Review(
            user_id=current_user_id,
            target_type=data['target_type'],
            target_id=data['target_id'],
            rating=data['rating'],
            title=data.get('title'),
            comment=data.get('comment'),
            images=data.get('images', []),
            is_anonymous=data.get('is_anonymous', False)
        )

        db.session.add(review)
        db.session.commit()

        return jsonify({'msg': '评论提交成功', 'review_id': review.id}), 201

# 用户中心命名空间
user_ns = api.namespace('user', description='用户中心相关接口')

@user_ns.route('/dashboard')
class UserDashboard(Resource):
    @jwt_required()
    @user_ns.response(200, '获取成功')
    def get(self):
        """获取用户仪表板数据"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        # 获取各类统计数据
        order_count = Order.query.filter_by(user_id=current_user_id).count()
        activity_count = UserActivity.query.filter_by(user_id=current_user_id).count()
        favorite_count = Favorite.query.filter_by(user_id=current_user_id).count()
        review_count = Review.query.filter_by(user_id=current_user_id).count()

        # 获取最近订单
        recent_orders = Order.query.filter_by(user_id=current_user_id).order_by(Order.created_at.desc()).limit(5).all()
        recent_orders_data = []
        for order in recent_orders:
            recent_orders_data.append({
                'id': order.id,
                'order_number': order.order_number,
                'order_type': order.order_type,
                'total_amount': float(order.total_amount),
                'order_status': order.order_status,
                'created_at': order.created_at.isoformat()
            })

        # 获取参与的活动
        user_activities = UserActivity.query.filter_by(user_id=current_user_id).order_by(UserActivity.created_at.desc()).limit(5).all()
        activities_data = []
        for ua in user_activities:
            activities_data.append({
                'id': ua.id,
                'activity': {
                    'id': ua.activity.id,
                    'title': ua.activity.title,
                    'start_time': ua.activity.start_time.isoformat(),
                    'location': ua.activity.location
                },
                'participation_status': ua.participation_status,
                'created_at': ua.created_at.isoformat()
            })

        return jsonify({
            'user': user.to_dict(),
            'stats': {
                'order_count': order_count,
                'activity_count': activity_count,
                'favorite_count': favorite_count,
                'review_count': review_count
            },
            'recent_orders': recent_orders_data,
            'recent_activities': activities_data
        }), 200

@user_ns.route('/favorites')
class UserFavorites(Resource):
    @jwt_required()
    @user_ns.response(200, '获取成功')
    def get(self):
        """获取用户收藏"""
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        target_type = request.args.get('type')

        query = Favorite.query.filter_by(user_id=current_user_id)
        if target_type:
            query = query.filter_by(target_type=target_type)

        favorites = query.order_by(Favorite.created_at.desc()).paginate(page=page, per_page=per_page)

        result = []
        for favorite in favorites.items:
            item_data = None
            if favorite.target_type == 'product':
                product = Product.query.get(favorite.target_id)
                if product:
                    item_data = {
                        'id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'images': product.images or [],
                        'category': product.category
                    }
            elif favorite.target_type == 'activity':
                activity = Activity.query.get(favorite.target_id)
                if activity:
                    item_data = {
                        'id': activity.id,
                        'title': activity.title,
                        'price': float(activity.price),
                        'start_time': activity.start_time.isoformat(),
                        'location': activity.location
                    }
            elif favorite.target_type == 'content':
                content = Content.query.get(favorite.target_id)
                if content:
                    item_data = {
                        'id': content.id,
                        'title': content.title,
                        'content_type': content.content_type,
                        'cover_image': content.cover_image
                    }

            if item_data:
                result.append({
                    'id': favorite.id,
                    'target_type': favorite.target_type,
                    'target_id': favorite.target_id,
                    'item': item_data,
                    'created_at': favorite.created_at.isoformat()
                })

        return jsonify({
            'favorites': result,
            'total': favorites.total,
            'pages': favorites.pages,
            'current_page': page
        }), 200

    @jwt_required()
    @user_ns.response(201, '收藏成功')
    @user_ns.response(400, '已经收藏过')
    def post(self):
        """添加收藏"""
        current_user_id = get_jwt_identity()
        data = request.get_json()

        target_type = data.get('target_type')
        target_id = data.get('target_id')

        if not target_type or not target_id:
            return jsonify({'msg': '需要指定收藏对象类型和ID'}), 400

        # 检查是否已经收藏
        existing = Favorite.query.filter_by(
            user_id=current_user_id,
            target_type=target_type,
            target_id=target_id
        ).first()

        if existing:
            return jsonify({'msg': '已经收藏过此内容'}), 400

        favorite = Favorite(
            user_id=current_user_id,
            target_type=target_type,
            target_id=target_id
        )

        db.session.add(favorite)
        db.session.commit()

        return jsonify({'msg': '收藏成功', 'favorite_id': favorite.id}), 201

@user_ns.route('/favorites/<int:favorite_id>')
class UserFavoriteResource(Resource):
    @jwt_required()
    @user_ns.response(200, '取消收藏成功')
    def delete(self, favorite_id):
        """取消收藏"""
        current_user_id = get_jwt_identity()
        favorite = Favorite.query.get(favorite_id)

        if not favorite or favorite.user_id != current_user_id:
            return jsonify({'msg': '收藏记录不存在'}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({'msg': '取消收藏成功'}), 200

# 支付集成命名空间
payment_ns = api.namespace('payments', description='支付相关接口')

@payment_ns.route('/create-payment')
class CreatePayment(Resource):
    @payment_ns.expect(api.model('PaymentRequest', {
        'order_id': fields.Integer(required=True, description='订单ID'),
        'payment_method': fields.String(required=True, enum=['wechat', 'alipay'], description='支付方式')
    }))
    @payment_ns.response(200, '支付创建成功')
    @payment_ns.response(404, '订单不存在')
    @jwt_required()
    def post(self):
        """创建支付"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        order_id = data.get('order_id')
        payment_method = data.get('payment_method', 'wechat')

        order = Order.query.get(order_id)
        if not order or order.user_id != current_user_id:
            return jsonify({'msg': '订单不存在'}), 404

        if order.payment_status == 'paid':
            return jsonify({'msg': '订单已支付'}), 400

        # 创建支付记录
        payment = Payment(
            order_id=order_id,
            payment_method=payment_method,
            amount=order.total_amount,
            transaction_id=f'{payment_method}_{order_id}_{int(datetime.utcnow().timestamp())}'
        )

        db.session.add(payment)
        db.session.commit()

        # 模拟支付成功（实际项目中需要集成真实支付）
        payment.payment_status = 'success'
        order.payment_status = 'paid'
        order.paid_at = datetime.utcnow()

        if order.order_type == 'activity':
            # 为活动订单创建参与记录
            for item in order.items:
                if item.item_type == 'activity':
                    user_activity = UserActivity(
                        user_id=current_user_id,
                        activity_id=item.item_id,
                        order_id=order.id,
                        participation_status='registered'
                    )
                    db.session.add(user_activity)

        db.session.commit()

        return jsonify({
            'msg': '支付成功',
            'payment_id': payment.id,
            'transaction_id': payment.transaction_id,
            'amount': float(payment.amount)
        }), 200

# 后台管理命名空间
admin_ns = api.namespace('admin', description='后台管理相关接口')

@admin_ns.route('/stats')
class AdminStats(Resource):
    @jwt_required()
    @admin_ns.response(200, '获取成功')
    def get(self):
        """获取后台统计数据"""
        # 用户统计
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        vip_users = User.query.filter_by(member_level='vip').count()
        premium_users = User.query.filter_by(member_level='premium').count()

        # 订单统计
        total_orders = Order.query.count()
        paid_orders = Order.query.filter_by(payment_status='paid').count()
        total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(Order.payment_status=='paid').scalar() or 0

        # 内容统计
        total_content = Content.query.count()
        published_content = Content.query.filter_by(status='published').count()

        # 活动统计
        total_activities = Activity.query.count()
        published_activities = Activity.query.filter_by(status='published').count()

        # 产品统计
        total_products = Product.query.count()
        available_products = Product.query.filter_by(is_available=True).count()

        return jsonify({
            'users': {
                'total': total_users,
                'active': active_users,
                'vip': vip_users,
                'premium': premium_users
            },
            'orders': {
                'total': total_orders,
                'paid': paid_orders,
                'revenue': float(total_revenue)
            },
            'content': {
                'total': total_content,
                'published': published_content
            },
            'activities': {
                'total': total_activities,
                'published': published_activities
            },
            'products': {
                'total': total_products,
                'available': available_products
            }
        }), 200

@admin_ns.route('/activities/review')
class AdminActivityReview(Resource):
    @jwt_required()
    @admin_ns.response(200, '获取成功')
    def get(self):
        """获取待审核活动列表"""
        activities = Activity.query.filter_by(review_status='pending').all()

        result = []
        for activity in activities:
            result.append({
                'id': activity.id,
                'title': activity.title,
                'description': activity.description,
                'activity_type': activity.activity_type,
                'organizer': {
                    'id': activity.organizer.id,
                    'username': activity.organizer.username,
                    'real_name': activity.organizer.real_name
                } if activity.organizer else None,
                'created_at': activity.created_at.isoformat()
            })

        return jsonify({'activities': result}), 200

@admin_ns.route('/activities/<int:activity_id>/review')
class AdminActivityReviewAction(Resource):
    @jwt_required()
    @admin_ns.expect(api.model('ReviewAction', {
        'action': fields.String(required=True, enum=['approve', 'reject'], description='审核动作'),
        'reason': fields.String(description='拒绝原因')
    }))
    @admin_ns.response(200, '审核完成')
    @admin_ns.response(404, '活动不存在')
    def put(self, activity_id):
        """审核活动"""
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'msg': '活动不存在'}), 404
        
        data = request.get_json()
        action = data.get('action')

        if action == 'approve':
            activity.review_status = 'approved'
            activity.status = 'published'
            activity.review_reason = None
        elif action == 'reject':
            activity.review_status = 'rejected'
            activity.status = 'draft'
            activity.review_reason = data.get('reason', '审核未通过')

        activity.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'msg': f'活动已{"通过" if action == "approve" else "拒绝"}审核'}), 200

@admin_ns.route('/content/review')
class AdminContentReview(Resource):
    @jwt_required()
    @admin_ns.response(200, '获取成功')
    def get(self):
        """获取待审核内容列表"""
        contents = Content.query.filter_by(status='draft').all()

        result = []
        for content in contents:
            result.append({
                'id': content.id,
                'title': content.title,
                'content_type': content.content_type,
                'author': {
                    'id': content.author.id,
                    'username': content.author.username,
                    'real_name': content.author.real_name
                } if content.author else None,
                'created_at': content.created_at.isoformat()
            })

        return jsonify({'contents': result}), 200

@admin_ns.route('/content/<int:content_id>/publish')
class AdminContentPublish(Resource):
    @jwt_required()
    @admin_ns.response(200, '发布成功')
    @admin_ns.response(404, '内容不存在')
    def put(self, content_id):
        """发布内容"""
        content = Content.query.get(content_id)
        if not content:
            return jsonify({'msg': '内容不存在'}), 404

        content.status = 'published'
        content.publish_time = datetime.utcnow()
        content.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'msg': '内容发布成功'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("芝栖养生平台数据库表创建完成")
        print("支持的文件上传类型:", ALLOWED_EXTENSIONS)
        print("上传文件大小限制: 16MB")
    app.run(
        debug=os.environ.get('FLASK_DEBUG') == '1',
        host='0.0.0.0',
        port=int(os.environ.get('FLASK_PORT', 5000))
    )
