# 芝栖养生平台前端

[![Vue.js](https://img.shields.io/badge/Vue.js-3.2.13-brightgreen.svg)](https://vuejs.org/)
[![Vue Router](https://img.shields.io/badge/Vue_Router-4.0.3-blue.svg)](https://router.vuejs.org/)
[![Vuex](https://img.shields.io/badge/Vuex-4.0.0-orange.svg)](https://vuex.vuejs.org/)
[![Axios](https://img.shields.io/badge/Axios-1.6.0-red.svg)](https://axios-http.com/)

> 🌿 基于 Vue.js 3 的现代化养生健康平台前端应用 🌿

## ✨ 核心功能

### 🏠 品牌首页
- **Hero区域**: 品牌故事 + 核心价值展示
- **功能矩阵**: 四大服务板块可视化
- **内容预览**: 热门文章和精选产品展示
- **服务承诺**: 品牌四大承诺展示

### 📚 内容中心
- **内容类型**: 文章、视频、科普、Vlog
- **分类浏览**: 按类型、分类筛选内容
- **搜索功能**: 全文搜索内容
- **互动功能**: 点赞、收藏、分享

### 🛍️ 养生产品
- **产品分类**: 灵芝产品、养生茶饮、孢子粉、文创周边、订阅盒
- **智能筛选**: 分类、价格、销量排序
- **产品详情**: 多图展示、溯源信息、用户评价
- **购物体验**: 购物车、立即购买、收藏商品

### 🎯 体验活动
- **活动类型**: 工坊体验、瑜伽课程、手作活动、采摘体验
- **活动状态**: 报名中、进行中、已结束
- **报名系统**: 在线报名、实时库存显示
- **参与跟踪**: 活动日程、签到反馈

### 🏞️ 体验基地
- **基地展示**: 接待展示区、静修住宿区、多功能工坊区、户外体验区
- **套餐预订**: "静心一夜"、"工坊周末"等标准化套餐
- **虚拟导览**: 基地环境、设施在线展示
- **位置服务**: 地图导航、路线规划

### 👤 用户中心
- **个人资料**: 基本信息、会员等级、积分展示
- **订单管理**: 产品订单、活动订单、住宿订单历史
- **活动参与**: 我的活动、参与记录、评价反馈
- **收藏管理**: 收藏的产品、活动、内容
- **消息通知**: 系统通知、活动提醒、订单状态

### ⚙️ 后台管理
- **内容审核**: 用户发布内容审核发布
- **活动管理**: 活动审核、状态管理、参与统计
- **订单处理**: 订单状态更新、退款处理、发货管理
- **用户管理**: 用户信息查看、会员管理、数据统计
- **数据分析**: 用户行为、销售数据、活动效果统计

## 🛠️ 技术架构

### 核心技术栈
- **框架**: Vue.js 3.2.13 (Composition API)
- **路由**: Vue Router 4.0.3 (懒加载 + 路由守卫)
- **状态管理**: Vuex 4.0.0 (模块化状态管理)
- **HTTP客户端**: Axios 1.6.0 (请求/响应拦截器)
- **样式**: 原生CSS + Flexbox/Grid (响应式设计)
- **构建工具**: Vue CLI 5.x (热重载 + 代码分割)

### 项目结构详解
```
frontend/
├── public/                     # 静态资源目录
│   ├── index.html             # HTML模板 (SEO优化)
│   └── favicon.ico            # 网站图标
├── src/                       # 源代码目录
│   ├── main.js               # 应用入口文件
│   ├── App.vue               # 根组件 (导航+页脚)
│   ├── components/           # 公共组件 (待开发)
│   │   ├── Loading.vue       # 加载组件
│   │   ├── Notification.vue  # 通知组件
│   │   ├── ProductCard.vue   # 产品卡片
│   │   └── ...
│   ├── views/                # 页面组件
│   │   ├── HomeView.vue      # 首页
│   │   ├── ProductList.vue   # 产品列表
│   │   ├── ContentList.vue   # 内容列表 (待开发)
│   │   ├── ActivityList.vue  # 活动列表 (待开发)
│   │   ├── BaseList.vue      # 基地列表 (待开发)
│   │   ├── UserDashboard.vue # 用户中心
│   │   ├── OrderList.vue     # 订单列表 (待开发)
│   │   ├── AdminDashboard.vue # 管理后台
│   │   └── ...
│   ├── router/               # 路由配置
│   │   └── index.js          # 路由定义 + 权限控制
│   ├── store/                # Vuex状态管理
│   │   ├── index.js          # 根store
│   │   ├── modules/          # 模块化store (待开发)
│   │   │   ├── user.js       # 用户模块
│   │   │   ├── cart.js       # 购物车模块
│   │   │   └── ...
│   │   └── getters.js        # 全局getters
│   └── utils/                # 工具函数 (待开发)
│       ├── api.js            # API封装
│       ├── auth.js           # 认证工具
│       └── validators.js     # 表单验证
├── tests/                    # 测试文件 (待开发)
│   ├── unit/                # 单元测试
│   └── e2e/                 # 端到端测试
├── package.json             # 项目配置
├── vue.config.js            # Vue CLI配置 (待创建)
└── README.md               # 项目文档
```

## 🚀 快速开始

### 环境要求
- **Node.js**: 14.0.0 或更高版本
- **npm**: 6.0.0 或更高版本
- **Vue CLI**: 5.0.0 或更高版本 (全局安装)

```bash
# 检查版本
node --version
npm --version

# 全局安装Vue CLI (如果未安装)
npm install -g @vue/cli
```

### 1. 克隆项目
```bash
git clone https://github.com/your-repo/zhiqi-wellness-platform.git
cd zhiqi-wellness-platform/frontend
```

### 2. 安装依赖
```bash
# 使用npm
npm install

# 或使用yarn (推荐)
yarn install

# 或使用pnpm
pnpm install
```

### 3. 配置环境变量
```bash
# 创建环境配置文件
cp .env.example .env.local

# 编辑 .env.local
VUE_APP_API_BASE_URL=http://localhost:5000
VUE_APP_ENV=development
```

### 4. 启动开发服务器
```bash
# 开发模式 (带热重载)
npm run serve

# 或指定端口
npm run serve -- --port 8080

# 访问 http://localhost:8080
```

### 5. 构建生产版本
```bash
# 构建优化版本
npm run build

# 预览构建结果
npm run preview

# 分析包大小
npm run analyze
```

## ⚙️ 开发配置

### Vue CLI配置 (vue.config.js)
```javascript
module.exports = {
  // 开发服务器配置
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  },

  // 构建配置
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          vue: {
            name: 'chunk-vue',
            test: /[\\/]node_modules[\\/]vue[\\/]/,
            priority: 20,
            chunks: 'initial'
          }
        }
      }
    }
  },

  // PWA配置 (可选)
  pwa: {
    name: '芝栖养生平台',
    themeColor: '#8b5a3c',
    msTileColor: '#8b5a3c'
  }
}
```

### 环境变量配置
```bash
# .env.development
VUE_APP_API_BASE_URL=http://localhost:5000
VUE_APP_ENV=development
VUE_APP_TITLE=芝栖养生平台 (开发版)

# .env.production
VUE_APP_API_BASE_URL=https://api.zhiqi-wellness.com
VUE_APP_ENV=production
VUE_APP_TITLE=芝栖养生平台
```

## 🎨 设计系统

### 品牌色彩
```scss
// 主题色彩
$primary-color: #8b5a3c;      // 灵芝棕 (主色)
$secondary-color: #a67c52;    // 浅棕色
$accent-color: #ffd700;       // 金黄色
$success-color: #8fbc8f;      // 自然绿
$warning-color: #f39c12;      // 橙色
$danger-color: #e74c3c;       // 红色

// 中性色彩
$text-primary: #2c3e50;       // 深灰
$text-secondary: #666666;     // 中灰
$text-muted: #999999;         // 浅灰
$border-color: #e9ecef;       // 边框色
$background: #fafafa;         // 背景色
```

### 响应式断点
```scss
$breakpoints: (
  xs: 0,      // 超小屏 (< 576px)
  sm: 576px,  // 小屏 (≥ 576px)
  md: 768px,  // 中屏 (≥ 768px)
  lg: 992px,  // 大屏 (≥ 992px)
  xl: 1200px, // 超大屏 (≥ 1200px)
  xxl: 1400px // 极大屏 (≥ 1400px)
);
```

### 组件样式规范
- **按钮**: 高度44px (移动端)、圆角20px
- **卡片**: 圆角12px、阴影效果
- **表单**: 统一高度、边框圆角
- **间距**: 8px网格系统

## 🔧 开发规范

### 命名规范
```javascript
// 组件命名 (PascalCase)
components/
  ├── ProductCard.vue
  ├── UserProfile.vue
  └── ActivityList.vue

// 文件命名 (kebab-case)
views/
  ├── product-list.vue
  ├── user-dashboard.vue
  └── activity-detail.vue

// 变量命名 (camelCase)
const userInfo = { ... }
const isLoading = false
const handleSubmit = () => { ... }
```

### 代码组织
```javascript
// 组件结构 (Vue 3 Composition API)
<template>
  <!-- 模板 -->
</template>

<script setup>
// 组合式API
import { ref, computed, onMounted } from 'vue'

// 响应式数据
const data = ref(null)
const loading = ref(false)

// 计算属性
const computedData = computed(() => {
  return data.value?.filter(item => item.active)
})

// 生命周期
onMounted(() => {
  fetchData()
})

// 方法
const fetchData = async () => {
  loading.value = true
  try {
    const response = await api.getData()
    data.value = response.data
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
// 样式
.component {
  &__header {
    // BEM命名规范
  }

  &__content {
    // 组件样式
  }
}
</style>
```

### 状态管理规范
```javascript
// store/modules/user.js
export default {
  namespaced: true,

  state: () => ({
    currentUser: null,
    profile: null
  }),

  mutations: {
    SET_USER(state, user) {
      state.currentUser = user
    },
    SET_PROFILE(state, profile) {
      state.profile = profile
    }
  },

  actions: {
    async fetchProfile({ commit }) {
      const response = await api.getProfile()
      commit('SET_PROFILE', response.data)
    }
  },

  getters: {
    isLoggedIn: state => !!state.currentUser,
    userRole: state => state.currentUser?.role || 'user'
  }
}
```

## 🧪 测试

### 单元测试
```bash
# 运行所有测试
npm run test:unit

# 运行特定测试
npm run test:unit -- --grep "UserProfile"

# 覆盖率报告
npm run test:unit -- --coverage
```

### E2E测试
```bash
# 运行E2E测试
npm run test:e2e

# 交互模式
npm run test:e2e:ui
```

## 🚀 部署

### 开发环境
```bash
npm run serve
```

### 生产环境
```bash
# 构建
npm run build

# 部署到Nginx
sudo cp -r dist/* /var/www/html/

# 或使用Docker
docker build -t zhiqi-frontend .
docker run -p 80:80 zhiqi-frontend
```

### CDN部署
```bash
# 静态资源上传到CDN
aws s3 sync dist/ s3://zhiqi-wellness-cdn --delete

# 或者使用阿里云OSS
aliyun oss cp dist/ oss://zhiqi-wellness/ -r
```

## 📊 性能优化

### 构建优化
- **代码分割**: 路由懒加载，按需加载组件
- **资源压缩**: Gzip压缩，图片优化
- **缓存策略**: 文件哈希，长期缓存
- **Tree Shaking**: 移除未使用代码

### 运行时优化
- **虚拟滚动**: 大列表虚拟化
- **图片懒加载**: 视口内图片优先加载
- **防抖节流**: 搜索、滚动事件优化
- **内存泄漏**: 组件销毁时清理定时器和事件监听

## 🔒 安全考虑

### 前端安全
- **XSS防护**: v-html内容过滤，CSP策略
- **CSRF防护**: Token验证，SameSite Cookie
- **内容安全**: 用户输入过滤和验证
- **HTTPS**: 强制HTTPS，证书配置

### 数据安全
- **敏感信息**: 不存储密码，Token安全存储
- **错误处理**: 不暴露敏感错误信息
- **日志记录**: 用户操作审计
- **数据验证**: 前端后端双重验证

## 📱 PWA支持 (可选)

### 清单文件 (public/manifest.json)
```json
{
  "name": "芝栖养生平台",
  "short_name": "芝栖养生",
  "description": "专业灵芝养生健康平台",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#8b5a3c",
  "background_color": "#ffffff",
  "icons": [
    {
      "src": "/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

### Service Worker
```javascript
// 注册Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
  })
}
```

## 🤝 贡献指南

### 开发流程
1. **创建分支**: `git checkout -b feature/new-feature`
2. **编写代码**: 遵循代码规范和最佳实践
3. **提交测试**: 确保所有测试通过
4. **代码审查**: 提交PR并等待审查
5. **合并主干**: 审查通过后合并到main分支

### 代码规范
- **ESLint**: 必须通过ESLint检查
- **Prettier**: 代码格式化
- **Commit规范**: 清晰的commit message
- **文档更新**: 新功能必须更新文档

## 📞 技术支持

- **开发文档**: [Vue.js官方文档](https://vuejs.org/)
- **UI组件**: [Element Plus](https://element-plus.org/)
- **状态管理**: [Vuex 4指南](https://vuex.vuejs.org/)
- **路由管理**: [Vue Router 4](https://router.vuejs.org/)

## 📄 开源协议

[MIT License](LICENSE)

---

<div align="center">

**芝栖养生平台前端** - 现代化Vue.js应用 🎉

⭐ 如果这个项目对你有帮助，请给我们一个star！

</div>