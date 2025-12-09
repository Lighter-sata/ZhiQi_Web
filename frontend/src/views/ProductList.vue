<template>
  <div class="product-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="container">
        <h1>养生产品</h1>
        <p>精选优质灵芝养生产品，让健康成为生活方式</p>
      </div>
    </div>

    <!-- 筛选和搜索区域 -->
    <div class="filters-section">
      <div class="container">
        <div class="filters-content">
          <!-- 分类筛选 -->
          <div class="filter-group">
            <label>产品分类：</label>
            <div class="filter-options">
              <button
                :class="['filter-btn', { active: selectedCategory === '' }]"
                @click="selectCategory('')"
              >
                全部
              </button>
              <button
                v-for="category in categories"
                :key="category.value"
                :class="['filter-btn', { active: selectedCategory === category.value }]"
                @click="selectCategory(category.value)"
              >
                {{ category.label }}
              </button>
            </div>
          </div>

          <!-- 搜索框 -->
          <div class="search-group">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索产品..."
              class="search-input"
              @keyup.enter="performSearch"
            >
            <button @click="performSearch" class="search-btn">搜索</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 产品列表 -->
    <div class="products-section">
      <div class="container">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <!-- 产品网格 -->
        <div v-else-if="products.length > 0" class="products-grid">
          <div
            v-for="product in products"
            :key="product.id"
            class="product-card"
            @click="goToProduct(product.id)"
          >
            <div class="product-image">
              <img
                :src="product.images?.[0] || defaultImage"
                :alt="product.name"
              >
              <div v-if="product.is_featured" class="product-badge">精选</div>
              <div class="product-overlay">
                <button
                  @click.stop="toggleFavorite(product)"
                  :class="['favorite-btn', { active: isFavorited('product', product.id) }]"
                >
                  ♥
                </button>
              </div>
            </div>

            <div class="product-info">
              <h3>{{ product.name }}</h3>
              <p class="product-description">{{ product.description }}</p>
              <div class="product-meta">
                <span class="category">{{ getCategoryLabel(product.category) }}</span>
                <span v-if="product.stock_quantity <= 10" class="stock-warning">
                  仅剩 {{ product.stock_quantity }} 件
                </span>
              </div>

              <div class="product-price">
                <span class="current-price">¥{{ product.price }}</span>
                <span v-if="product.original_price" class="original-price">
                  ¥{{ product.original_price }}
                </span>
              </div>

              <div class="product-actions">
                <button
                  @click.stop="addToCart(product)"
                  class="btn btn-primary btn-sm"
                  :disabled="product.stock_quantity <= 0"
                >
                  {{ product.stock_quantity > 0 ? '加入购物车' : '缺货' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <div class="empty-icon">🛍️</div>
          <h3>暂无产品</h3>
          <p>该分类下还没有产品，敬请期待</p>
        </div>

        <!-- 分页 -->
        <div v-if="totalPages > 1" class="pagination">
          <button
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage <= 1"
            class="page-btn"
          >
            上一页
          </button>

          <span
            v-for="page in visiblePages"
            :key="page"
            :class="['page-btn', { active: page === currentPage }]"
            @click="goToPage(page)"
          >
            {{ page }}
          </span>

          <button
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage >= totalPages"
            class="page-btn"
          >
            下一页
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductList',
  data() {
    return {
      products: [],
      loading: false,
      selectedCategory: '',
      searchQuery: '',
      currentPage: 1,
      totalPages: 1,
      totalProducts: 0,
      defaultImage: 'https://via.placeholder.com/300x300/8b5a3c/ffffff?text=养生产品',
      categories: [
        { value: 'lingzhi', label: '灵芝产品' },
        { value: 'tea', label: '养生茶饮' },
        { value: 'spore', label: '孢子粉' },
        { value: 'gift', label: '文创周边' },
        { value: 'subscription', label: '订阅盒' }
      ]
    };
  },
  computed: {
    visiblePages() {
      const pages = [];
      const start = Math.max(1, this.currentPage - 2);
      const end = Math.min(this.totalPages, this.currentPage + 2);

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      return pages;
    }
  },
  mounted() {
    this.loadProducts();
  },
  watch: {
    '$route.query': {
      handler() {
        this.selectedCategory = this.$route.query.category || '';
        this.searchQuery = this.$route.query.search || '';
        this.currentPage = parseInt(this.$route.query.page) || 1;
        this.loadProducts();
      },
      immediate: true
    }
  },
  methods: {
    async loadProducts() {
      this.loading = true;

      try {
        const params = {
          page: this.currentPage,
          per_page: 12
        };

        if (this.selectedCategory) {
          params.category = this.selectedCategory;
        }

        if (this.searchQuery) {
          params.search = this.searchQuery;
        }

        const response = await axios.get('/api/products/', { params });
        const data = response.data;

        this.products = data.products || [];
        this.totalPages = data.pages || 1;
        this.totalProducts = data.total || 0;

      } catch (error) {
        console.error('加载产品失败:', error);
        this.$store.dispatch('addNotification', {
          type: 'error',
          title: '加载失败',
          message: '无法加载产品列表，请稍后重试'
        });

        // 使用模拟数据
        this.products = [
          {
            id: 1,
            name: '野生灵芝片',
            description: '精选野生灵芝，传统工艺加工，保留灵芝精华',
            category: 'lingzhi',
            price: 299,
            original_price: 399,
            stock_quantity: 50,
            is_featured: true,
            images: []
          },
          {
            id: 2,
            name: '七味养生茶包',
            description: '七种名贵中药材精心配方，日常养生必备',
            category: 'tea',
            price: 128,
            original_price: null,
            stock_quantity: 5,
            is_featured: false,
            images: []
          }
        ];
        this.totalPages = 1;
        this.totalProducts = 2;
      } finally {
        this.loading = false;
      }
    },

    selectCategory(category) {
      this.selectedCategory = category;
      this.currentPage = 1;
      this.updateQuery();
    },

    performSearch() {
      this.currentPage = 1;
      this.updateQuery();
    },

    updateQuery() {
      const query = {};

      if (this.selectedCategory) {
        query.category = this.selectedCategory;
      }

      if (this.searchQuery) {
        query.search = this.searchQuery;
      }

      if (this.currentPage > 1) {
        query.page = this.currentPage;
      }

      this.$router.push({ query });
    },

    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.updateQuery();
      }
    },

    getCategoryLabel(category) {
      const categoryMap = {
        lingzhi: '灵芝产品',
        tea: '养生茶饮',
        spore: '孢子粉',
        gift: '文创周边',
        subscription: '订阅盒'
      };
      return categoryMap[category] || category;
    },

    goToProduct(id) {
      this.$router.push(`/products/${id}`);
    },

    toggleFavorite(product) {
      if (!this.$store.getters.isAuthenticated) {
        this.$store.dispatch('addNotification', {
          type: 'warning',
          title: '请先登录',
          message: '登录后即可收藏产品'
        });
        this.$router.push('/login');
        return;
      }

      const isFavorited = this.isFavorited('product', product.id);
      const favoriteItem = {
        type: 'product',
        id: product.id,
        name: product.name,
        image: product.images?.[0] || this.defaultImage,
        price: product.price
      };

      if (isFavorited) {
        this.$store.dispatch('removeFromFavorites', { type: 'product', id: product.id });
        this.$store.dispatch('addNotification', {
          type: 'success',
          title: '已取消收藏',
          message: `${product.name} 已从收藏中移除`
        });
      } else {
        this.$store.dispatch('addToFavorites', favoriteItem);
        this.$store.dispatch('addNotification', {
          type: 'success',
          title: '收藏成功',
          message: `${product.name} 已添加到收藏`
        });
      }
    },

    isFavorited(type, id) {
      return this.$store.getters.isFavorited(type, id);
    },

    addToCart(product) {
      if (product.stock_quantity <= 0) {
        this.$store.dispatch('addNotification', {
          type: 'warning',
          title: '库存不足',
          message: '该产品暂时缺货'
        });
        return;
      }

      const cartItem = {
        type: 'product',
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.images?.[0] || this.defaultImage,
        quantity: 1
      };

      this.$store.dispatch('addToCart', cartItem);
      this.$store.dispatch('addNotification', {
        type: 'success',
        title: '添加成功',
        message: `${product.name} 已添加到购物车`
      });
    }
  }
};
</script>

<style scoped>
/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #8b5a3c 0%, #a67c52 100%);
  color: white;
  padding: 60px 0;
  text-align: center;
}

.page-header h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.page-header p {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
}

/* 筛选区域 */
.filters-section {
  background: white;
  border-bottom: 1px solid #e9ecef;
  padding: 30px 0;
}

.filters-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 15px;
}

.filter-group label {
  font-weight: 500;
  color: #2c3e50;
  white-space: nowrap;
}

.filter-options {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  color: #666;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.filter-btn:hover {
  border-color: #8b5a3c;
  color: #8b5a3c;
}

.filter-btn.active {
  background: #8b5a3c;
  color: white;
  border-color: #8b5a3c;
}

.search-group {
  display: flex;
  gap: 10px;
  min-width: 300px;
}

.search-input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 25px;
  font-size: 0.9rem;
}

.search-input:focus {
  outline: none;
  border-color: #8b5a3c;
}

.search-btn {
  padding: 10px 20px;
  background: #8b5a3c;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.search-btn:hover {
  background: #a67c52;
}

/* 产品区域 */
.products-section {
  padding: 60px 0;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.product-image {
  position: relative;
  height: 250px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #ff6b6b;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.product-overlay {
  position: absolute;
  top: 12px;
  right: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .product-overlay {
  opacity: 1;
}

.favorite-btn {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.1);
}

.favorite-btn.active {
  color: #e74c3c;
}

.product-info {
  padding: 20px;
}

.product-info h3 {
  font-size: 1.1rem;
  color: #2c3e50;
  margin-bottom: 8px;
  line-height: 1.4;
}

.product-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-size: 0.8rem;
}

.category {
  color: #8b5a3c;
  background: rgba(139, 90, 60, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
}

.stock-warning {
  color: #e67e22;
  font-weight: 500;
}

.product-price {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.current-price {
  font-size: 1.3rem;
  font-weight: 600;
  color: #e74c3c;
}

.original-price {
  font-size: 1rem;
  color: #999;
  text-decoration: line-through;
}

.product-actions {
  text-align: center;
}

/* 按钮样式 */
.btn {
  padding: 10px 20px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  text-align: center;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #8b5a3c, #a67c52);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #a67c52, #b89a6a);
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 0.9rem;
}

/* 加载状态 */
.loading {
  text-align: center;
  padding: 60px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #8b5a3c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 0;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h3 {
  color: #666;
  margin-bottom: 10px;
}

.empty-state p {
  color: #999;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 40px;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  color: #666;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  border-color: #8b5a3c;
  color: #8b5a3c;
}

.page-btn.active {
  background: #8b5a3c;
  color: white;
  border-color: #8b5a3c;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }

  .filters-content {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    justify-content: center;
  }

  .filter-options {
    justify-content: center;
  }

  .search-group {
    min-width: auto;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }

  .product-info {
    padding: 15px;
  }
}
</style>
