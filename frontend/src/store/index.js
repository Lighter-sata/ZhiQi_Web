import { createStore } from 'vuex';

export default createStore({
  state: {
    // 用户认证状态
    isAuthenticated: !!localStorage.getItem('access_token'),
    user: null,
    token: localStorage.getItem('access_token'),

    // 购物车
    cart: {
      items: [],
      total: 0
    },

    // 收藏列表
    favorites: [],

    // 全局加载状态
    loading: false,

    // 消息通知
    notifications: [],

    // 搜索历史
    searchHistory: []
  },

  mutations: {
    // 用户认证相关
    setAuthenticated(state, status) {
      state.isAuthenticated = status;
    },
    setUser(state, userData) {
      state.user = userData;
      if (userData) {
        localStorage.setItem('user', JSON.stringify(userData));
      } else {
        localStorage.removeItem('user');
      }
    },
    setToken(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem('access_token', token);
      } else {
        localStorage.removeItem('access_token');
      }
    },

    // 购物车相关
    addToCart(state, item) {
      const existingItem = state.cart.items.find(cartItem =>
        cartItem.type === item.type && cartItem.id === item.id
      );

      if (existingItem) {
        existingItem.quantity += item.quantity || 1;
      } else {
        state.cart.items.push({
          ...item,
          quantity: item.quantity || 1
        });
      }

      state.cart.total = state.cart.items.reduce((total, cartItem) =>
        total + (cartItem.price * cartItem.quantity), 0
      );

      // 保存到localStorage
      localStorage.setItem('cart', JSON.stringify(state.cart));
    },

    removeFromCart(state, { type, id }) {
      state.cart.items = state.cart.items.filter(item =>
        !(item.type === type && item.id === id)
      );

      state.cart.total = state.cart.items.reduce((total, item) =>
        total + (item.price * item.quantity), 0
      );

      localStorage.setItem('cart', JSON.stringify(state.cart));
    },

    updateCartItem(state, { type, id, quantity }) {
      const item = state.cart.items.find(item =>
        item.type === type && item.id === id
      );

      if (item) {
        item.quantity = quantity;
        state.cart.total = state.cart.items.reduce((total, cartItem) =>
          total + (cartItem.price * cartItem.quantity), 0
        );

        localStorage.setItem('cart', JSON.stringify(state.cart));
      }
    },

    clearCart(state) {
      state.cart = { items: [], total: 0 };
      localStorage.removeItem('cart');
    },

    loadCart(state) {
      const cartStr = localStorage.getItem('cart');
      if (cartStr) {
        try {
          state.cart = JSON.parse(cartStr);
        } catch (e) {
          console.error('解析购物车数据失败:', e);
        }
      }
    },

    // 收藏相关
    addToFavorites(state, item) {
      const exists = state.favorites.find(fav =>
        fav.type === item.type && fav.id === item.id
      );

      if (!exists) {
        state.favorites.push(item);
        localStorage.setItem('favorites', JSON.stringify(state.favorites));
      }
    },

    removeFromFavorites(state, { type, id }) {
      state.favorites = state.favorites.filter(fav =>
        !(fav.type === type && fav.id === id)
      );

      localStorage.setItem('favorites', JSON.stringify(state.favorites));
    },

    loadFavorites(state) {
      const favoritesStr = localStorage.getItem('favorites');
      if (favoritesStr) {
        try {
          state.favorites = JSON.parse(favoritesStr);
        } catch (e) {
          console.error('解析收藏数据失败:', e);
        }
      }
    },

    // 全局状态
    setLoading(state, loading) {
      state.loading = loading;
    },

    // 通知相关
    addNotification(state, notification) {
      state.notifications.unshift({
        id: Date.now(),
        ...notification
      });
    },

    removeNotification(state, id) {
      state.notifications = state.notifications.filter(notif => notif.id !== id);
    },

    clearNotifications(state) {
      state.notifications = [];
    },

    // 搜索历史
    addSearchHistory(state, keyword) {
      const index = state.searchHistory.indexOf(keyword);
      if (index > -1) {
        state.searchHistory.splice(index, 1);
      }
      state.searchHistory.unshift(keyword);
      if (state.searchHistory.length > 10) {
        state.searchHistory = state.searchHistory.slice(0, 10);
      }
      localStorage.setItem('searchHistory', JSON.stringify(state.searchHistory));
    },

    clearSearchHistory(state) {
      state.searchHistory = [];
      localStorage.removeItem('searchHistory');
    },

    loadSearchHistory(state) {
      const historyStr = localStorage.getItem('searchHistory');
      if (historyStr) {
        try {
          state.searchHistory = JSON.parse(historyStr);
        } catch (e) {
          console.error('解析搜索历史失败:', e);
        }
      }
    }
  },

  actions: {
    // 用户认证
    async login({ commit, dispatch }, credentials) {
      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(credentials)
        });

        const data = await response.json();

        if (response.ok) {
          commit('setToken', data.access_token);
          commit('setAuthenticated', true);

          // 解析token获取用户信息（简化版）
          const userResponse = await fetch('/api/auth/profile', {
            headers: {
              'Authorization': `Bearer ${data.access_token}`
            }
          });

          if (userResponse.ok) {
            const userData = await userResponse.json();
            commit('setUser', userData.user);
          }

          dispatch('loadUserData');
        }

        return data;
      } catch (error) {
        console.error('登录失败:', error);
        throw error;
      }
    },

    async logout({ commit }) {
      commit('setToken', null);
      commit('setAuthenticated', false);
      commit('setUser', null);
      commit('clearCart');
      commit('clearNotifications');
    },

    // 加载用户相关数据
    loadUserData({ commit }) {
      commit('loadCart');
      commit('loadFavorites');
      commit('loadSearchHistory');
    },

    // 购物车操作
    addToCart({ commit }, item) {
      commit('addToCart', item);
    },

    removeFromCart({ commit }, item) {
      commit('removeFromCart', item);
    },

    updateCartItem({ commit }, item) {
      commit('updateCartItem', item);
    },

    clearCart({ commit }) {
      commit('clearCart');
    },

    // 收藏操作
    addToFavorites({ commit }, item) {
      commit('addToFavorites', item);
    },

    removeFromFavorites({ commit }, item) {
      commit('removeFromFavorites', item);
    },

    // 消息通知
    addNotification({ commit }, notification) {
      commit('addNotification', notification);
      // 自动清除通知
      setTimeout(() => {
        commit('removeNotification', notification.id || Date.now());
      }, 5000);
    },

    // 搜索历史
    addSearchHistory({ commit }, keyword) {
      commit('addSearchHistory', keyword);
    },

    clearSearchHistory({ commit }) {
      commit('clearSearchHistory');
    }
  },

  getters: {
    // 用户状态
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
    userRole: state => state.user?.role || 'user',

    // 购物车
    cartItems: state => state.cart.items,
    cartTotal: state => state.cart.total,
    cartItemCount: state => state.cart.items.reduce((total, item) => total + item.quantity, 0),

    // 收藏
    favorites: state => state.favorites,
    isFavorited: state => (type, id) => {
      return state.favorites.some(fav => fav.type === type && fav.id === id);
    },

    // 全局状态
    loading: state => state.loading,

    // 通知
    notifications: state => state.notifications,
    unreadNotifications: state => state.notifications.filter(n => !n.read),

    // 搜索历史
    searchHistory: state => state.searchHistory
  }
});