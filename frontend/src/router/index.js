import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  // 首页
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '../views/HomeView.vue'),
  },

  // 用户认证
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "register" */ '../views/Register.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue'),
  },

  // 内容中心
  {
    path: '/content',
    name: 'ContentList',
    component: () => import(/* webpackChunkName: "content-list" */ '../views/ContentList.vue'),
  },
  {
    path: '/content/:id',
    name: 'ContentDetail',
    component: () => import(/* webpackChunkName: "content-detail" */ '../views/ContentDetail.vue'),
    props: true,
  },

  // 产品中心
  {
    path: '/products',
    name: 'ProductList',
    component: () => import(/* webpackChunkName: "product-list" */ '../views/ProductList.vue'),
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: () => import(/* webpackChunkName: "product-detail" */ '../views/ProductDetail.vue'),
    props: true,
  },

  // 活动中心
  {
    path: '/activities',
    name: 'ActivityList',
    component: () => import(/* webpackChunkName: "activity-list" */ '../views/ActivityList.vue'),
  },
  {
    path: '/activities/:id',
    name: 'ActivityDetail',
    component: () => import(/* webpackChunkName: "activity-detail" */ '../views/ActivityDetail.vue'),
    props: true,
  },
  {
    path: '/activities/create',
    name: 'ActivityCreate',
    component: () => import(/* webpackChunkName: "activity-create" */ '../views/ActivityCreate.vue'),
    meta: { requiresAuth: true },
  },

  // 体验基地
  {
    path: '/bases',
    name: 'BaseList',
    component: () => import(/* webpackChunkName: "base-list" */ '../views/BaseList.vue'),
  },
  {
    path: '/bases/:id',
    name: 'BaseDetail',
    component: () => import(/* webpackChunkName: "base-detail" */ '../views/BaseDetail.vue'),
    props: true,
  },

  // 用户中心
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: () => import(/* webpackChunkName: "user-dashboard" */ '../views/UserDashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/orders',
    name: 'OrderList',
    component: () => import(/* webpackChunkName: "order-list" */ '../views/OrderList.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/orders/:id',
    name: 'OrderDetail',
    component: () => import(/* webpackChunkName: "order-detail" */ '../views/OrderDetail.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/favorites',
    name: 'UserFavorites',
    component: () => import(/* webpackChunkName: "user-favorites" */ '../views/UserFavorites.vue'),
    meta: { requiresAuth: true },
  },

  // 后台管理
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import(/* webpackChunkName: "admin-dashboard" */ '../views/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/content',
    name: 'AdminContent',
    component: () => import(/* webpackChunkName: "admin-content" */ '../views/AdminContent.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/activities',
    name: 'AdminActivities',
    component: () => import(/* webpackChunkName: "admin-activities" */ '../views/AdminActivities.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/orders',
    name: 'AdminOrders',
    component: () => import(/* webpackChunkName: "admin-orders" */ '../views/AdminOrders.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import(/* webpackChunkName: "admin-users" */ '../views/AdminUsers.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },

  // 其他页面
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token');

  // 解析用户角色（简化版，实际项目中应该从token中解析）
  let userRole = null;
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      const user = JSON.parse(userStr);
      userRole = user.role || 'user';
    } catch (e) {
      console.error('解析用户信息失败:', e);
    }
  }

  const isAdmin = userRole === 'admin';

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresAdmin && !isAdmin) {
    alert('需要管理员权限访问');
    next('/');
  } else {
    next();
  }
});

export default router;