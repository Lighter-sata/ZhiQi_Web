import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';

// 配置axios
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

// 请求拦截器 - 添加认证token
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理认证错误
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response?.status === 401) {
      // token过期或无效，清除登录状态
      store.dispatch('logout');
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

// 创建Vue应用实例
const app = createApp(App);

// 全局配置
app.config.globalProperties.$axios = axios;

// 使用插件
app.use(router);
app.use(store);

// 挂载应用
app.mount('#app');