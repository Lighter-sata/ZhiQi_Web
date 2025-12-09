<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <header class="main-header">
      <nav class="navbar">
        <div class="nav-container">
          <!-- 品牌Logo -->
          <div class="brand">
            <router-link to="/" class="brand-link">
              <div class="brand-logo">
                <span class="brand-icon">芝</span>
              </div>
              <div class="brand-text">
                <h1>芝栖养生</h1>
                <p>ZhiQi Wellness</p>
              </div>
            </router-link>
          </div>

          <!-- 主要导航菜单 -->
          <ul class="nav-menu">
            <li><router-link to="/" exact>首页</router-link></li>
            <li><router-link to="/content">内容中心</router-link></li>
            <li><router-link to="/products">养生产品</router-link></li>
            <li><router-link to="/activities">体验活动</router-link></li>
            <li><router-link to="/bases">体验基地</router-link></li>
          </ul>

          <!-- 用户菜单 -->
          <div class="user-menu" v-if="isLoggedIn">
            <div class="user-dropdown">
              <button class="user-btn" @click="toggleUserMenu">
                <img v-if="user.avatar" :src="user.avatar" class="user-avatar" alt="头像">
                <div v-else class="user-avatar-placeholder">
                  {{ user.username ? user.username.charAt(0).toUpperCase() : 'U' }}
                </div>
                <span class="user-name">{{ user.real_name || user.username }}</span>
                <i class="dropdown-icon" :class="{ 'rotated': showUserMenu }">▼</i>
              </button>
              <div class="dropdown-menu" v-show="showUserMenu">
                <router-link to="/dashboard" class="dropdown-item">个人中心</router-link>
                <router-link to="/orders" class="dropdown-item">我的订单</router-link>
                <router-link to="/favorites" class="dropdown-item">我的收藏</router-link>
                <div class="dropdown-divider"></div>
                <a href="#" @click.prevent="logout" class="dropdown-item">退出登录</a>
              </div>
            </div>
          </div>

          <!-- 登录注册按钮 -->
          <div class="auth-buttons" v-else>
            <router-link to="/login" class="btn btn-outline">登录</router-link>
            <router-link to="/register" class="btn btn-primary">注册</router-link>
          </div>
        </div>
      </nav>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <router-view/>
    </main>

    <!-- 页脚 -->
    <footer class="main-footer">
      <div class="footer-container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>芝栖养生</h3>
            <p>专业灵芝养生健康平台，致力于为您提供优质的养生产品和体验服务。</p>
          </div>
          <div class="footer-section">
            <h4>快速链接</h4>
            <ul>
              <li><router-link to="/products">养生产品</router-link></li>
              <li><router-link to="/activities">体验活动</router-link></li>
              <li><router-link to="/bases">体验基地</router-link></li>
              <li><router-link to="/content">内容中心</router-link></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>联系我们</h4>
            <p>📧 contact@zhiqi.com</p>
            <p>📱 400-888-8888</p>
            <p>🏠 北京市朝阳区灵芝路88号</p>
          </div>
          <div class="footer-section">
            <h4>关注我们</h4>
            <div class="social-links">
              <a href="#" class="social-link">微信</a>
              <a href="#" class="social-link">微博</a>
              <a href="#" class="social-link">抖音</a>
              <a href="#" class="social-link">小红书</a>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2024 芝栖养生平台. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      showUserMenu: false,
      user: {}
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('access_token');
    }
  },
  mounted() {
    // 从localStorage获取用户信息
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        this.user = JSON.parse(userStr);
      } catch (e) {
        console.error('解析用户信息失败:', e);
      }
    }

    // 点击其他地方关闭下拉菜单
    document.addEventListener('click', this.closeUserMenu);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeUserMenu);
  },
  methods: {
    toggleUserMenu(event) {
      event.stopPropagation();
      this.showUserMenu = !this.showUserMenu;
    },
    closeUserMenu() {
      this.showUserMenu = false;
    },
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      this.user = {};
      this.showUserMenu = false;
      this.$router.push('/login');
    }
  }
};
</script>

<style>
/* 全局样式重置和基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'PingFang SC', 'Helvetica Neue', STHeiti, 'Microsoft Yahei', sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #fafafa;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 导航栏样式 */
.main-header {
  background: linear-gradient(135deg, #8b5a3c 0%, #a67c52 100%);
  box-shadow: 0 2px 10px rgba(139, 90, 60, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar {
  padding: 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

/* 品牌样式 */
.brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
}

.brand-logo {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  font-size: 24px;
  font-weight: bold;
}

.brand-text h1 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
  color: white;
}

.brand-text p {
  font-size: 12px;
  margin: 0;
  opacity: 0.8;
  color: white;
}

/* 导航菜单 */
.nav-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-menu li {
  margin: 0 15px;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-menu a:hover,
.nav-menu a.router-link-exact-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* 用户菜单 */
.user-menu {
  position: relative;
}

.user-btn {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 20px;
  transition: background 0.3s ease;
}

.user-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 8px;
}

.user-avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 8px;
}

.user-name {
  margin-right: 8px;
  font-weight: 500;
}

.dropdown-icon {
  font-size: 12px;
  transition: transform 0.3s ease;
}

.dropdown-icon.rotated {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-width: 160px;
  margin-top: 8px;
  overflow: hidden;
}

.dropdown-item {
  display: block;
  padding: 12px 16px;
  color: #333;
  text-decoration: none;
  transition: background 0.3s ease;
}

.dropdown-item:hover {
  background: #f8f9fa;
}

.dropdown-divider {
  height: 1px;
  background: #e9ecef;
  margin: 4px 0;
}

/* 认证按钮 */
.auth-buttons {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 8px 20px;
  border-radius: 20px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  text-align: center;
}

.btn-outline {
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
}

.btn-primary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-primary:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  min-height: calc(100vh - 70px - 300px);
}

/* 页脚样式 */
.main-footer {
  background: #2c3e50;
  color: white;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.footer-section h3 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #a67c52;
}

.footer-section h4 {
  font-size: 16px;
  margin-bottom: 15px;
}

.footer-section p {
  margin-bottom: 8px;
  opacity: 0.8;
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: 8px;
}

.footer-section a {
  color: white;
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.footer-section a:hover {
  opacity: 1;
}

.social-links {
  display: flex;
  gap: 15px;
}

.social-link {
  color: white;
  text-decoration: none;
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
  text-align: center;
}

.footer-bottom p {
  opacity: 0.6;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    height: auto;
    padding: 15px 20px;
  }

  .brand {
    margin-bottom: 15px;
  }

  .nav-menu {
    margin: 15px 0;
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-menu li {
    margin: 5px 10px;
  }

  .user-menu,
  .auth-buttons {
    margin-top: 15px;
  }

  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
</style>