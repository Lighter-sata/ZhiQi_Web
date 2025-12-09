<template>
  <div class="content-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="container">
        <h1>内容中心</h1>
        <p>专业养生科普，生活方式分享，发现健康美好生活</p>
      </div>
    </div>

    <!-- 内容筛选 -->
    <div class="filters-section">
      <div class="container">
        <div class="filters-content">
          <!-- 内容类型筛选 -->
          <div class="filter-group">
            <label>内容类型：</label>
            <div class="filter-options">
              <button
                :class="['filter-btn', { active: selectedType === '' }]"
                @click="selectType('')"
              >
                全部
              </button>
              <button
                v-for="type in contentTypes"
                :key="type.value"
                :class="['filter-btn', { active: selectedType === type.value }]"
                @click="selectType(type.value)"
              >
                {{ type.label }}
              </button>
            </div>
          </div>

          <!-- 分类筛选 -->
          <div class="filter-group">
            <label>分类：</label>
            <select v-model="selectedCategory" @change="loadContent" class="category-select">
              <option value="">全部分类</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <!-- 搜索框 -->
          <div class="search-group">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索内容..."
              class="search-input"
              @keyup.enter="performSearch"
            >
            <button @click="performSearch" class="search-btn">搜索</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 内容列表 -->
    <div class="content-section">
      <div class="container">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <!-- 内容网格 -->
        <div v-else-if="contents.length > 0" class="content-grid">
          <div
            v-for="content in contents"
            :key="content.id"
            class="content-card"
            @click="goToContent(content.id)"
          >
            <div class="content-image">
              <img :src="content.cover_image || defaultImage" :alt="content.title">
              <div class="content-type">{{ getContentTypeText(content.content_type) }}</div>
            </div>

            <div class="content-info">
              <h3>{{ content.title }}</h3>
              <p class="content-summary">{{ content.summary }}</p>

              <div class="content-meta">
                <span class="author">{{ content.author?.real_name || '芝栖养生' }}</span>
                <span class="date">{{ formatDate(content.created_at) }}</span>
                <span class="views">{{ content.views_count }} 阅读</span>
              </div>

              <div class="content-stats">
                <span class="likes">👍 {{ content.likes_count }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <div class="empty-icon">📚</div>
          <h3>暂无内容</h3>
          <p>该分类下还没有内容，敬请期待</p>
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
import axios from 'axios'

export default {
  name: 'ContentList',
  data() {
    return {
      contents: [],
      loading: false,
      selectedType: '',
      selectedCategory: '',
      searchQuery: '',
      currentPage: 1,
      totalPages: 1,
      totalContents: 0,
      defaultImage: 'https://via.placeholder.com/400x250/8b5a3c/ffffff?text=养生内容',
      contentTypes: [
        { value: 'article', label: '文章' },
        { value: 'video', label: '视频' },
        { value: 'knowledge', label: '科普' },
        { value: 'vlog', label: 'Vlog' }
      ],
      categories: ['灵芝知识', '养生方法', '健康生活', '品牌故事']
    }
  },
  computed: {
    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end = Math.min(this.totalPages, this.currentPage + 2)

      for (let i = start; i <= end; i++) {
        pages.push(i)
      }

      return pages
    }
  },
  mounted() {
    this.loadContent()
  },
  watch: {
    '$route.query': {
      handler() {
        this.selectedType = this.$route.query.type || ''
        this.selectedCategory = this.$route.query.category || ''
        this.searchQuery = this.$route.query.search || ''
        this.currentPage = parseInt(this.$route.query.page) || 1
        this.loadContent()
      },
      immediate: true
    }
  },
  methods: {
    async loadContent() {
      this.loading = true

      try {
        const params = {
          page: this.currentPage,
          per_page: 12
        }

        if (this.selectedType) {
          params.content_type = this.selectedType
        }

        if (this.selectedCategory) {
          params.category = this.selectedCategory
        }

        if (this.searchQuery) {
          params.search = this.searchQuery
        }

        const response = await axios.get('/api/content/', { params })
        const data = response.data

        this.contents = data.contents || []
        this.totalPages = data.pages || 1
        this.totalContents = data.total || 0

      } catch (error) {
        console.error('加载内容失败:', error)
        this.$store.dispatch('addNotification', {
          type: 'error',
          title: '加载失败',
          message: '无法加载内容列表，请稍后重试'
        })

        // 使用模拟数据
        this.contents = [
          {
            id: 1,
            title: '3分钟看懂孢子粉破壁技术',
            content_type: 'knowledge',
            summary: '孢子粉破壁技术是现代灵芝加工的重要突破，让我们用3分钟时间来了解这项技术...',
            cover_image: null,
            views_count: 1250,
            likes_count: 89,
            created_at: '2024-12-08T10:00:00Z',
            author: { real_name: '芝栖养生' }
          },
          {
            id: 2,
            title: '灵芝养生生活方式分享',
            content_type: 'vlog',
            summary: '跟随我们的Vlog，一起探索灵芝养生的魅力，发现健康生活的新方式...',
            cover_image: null,
            views_count: 890,
            likes_count: 67,
            created_at: '2024-12-07T15:30:00Z',
            author: { real_name: '芝栖养生' }
          },
          {
            id: 3,
            title: '冬日养生指南：灵芝暖身汤',
            content_type: 'article',
            summary: '冬季是养生的黄金季节，一碗热腾腾的灵芝暖身汤，不仅暖胃还暖心...',
            cover_image: null,
            views_count: 654,
            likes_count: 45,
            created_at: '2024-12-06T09:15:00Z',
            author: { real_name: '芝栖养生' }
          }
        ]
        this.totalPages = 1
        this.totalContents = 3
      } finally {
        this.loading = false
      }
    },

    selectType(type) {
      this.selectedType = type
      this.currentPage = 1
      this.updateQuery()
    },

    performSearch() {
      this.currentPage = 1
      this.updateQuery()
    },

    updateQuery() {
      const query = {}

      if (this.selectedType) {
        query.type = this.selectedType
      }

      if (this.selectedCategory) {
        query.category = this.selectedCategory
      }

      if (this.searchQuery) {
        query.search = this.searchQuery
      }

      if (this.currentPage > 1) {
        query.page = this.currentPage
      }

      this.$router.push({ query })
    },

    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.updateQuery()
      }
    },

    getContentTypeText(type) {
      const types = {
        article: '文章',
        video: '视频',
        knowledge: '科普',
        vlog: 'Vlog'
      }
      return types[type] || type
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },

    goToContent(id) {
      this.$router.push(`/content/${id}`)
    }
  }
}
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
  flex-wrap: wrap;
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

.category-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  min-width: 120px;
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

/* 内容区域 */
.content-section {
  padding: 60px 0;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.content-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.content-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.content-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.content-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.content-card:hover .content-image img {
  transform: scale(1.05);
}

.content-type {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(139, 90, 60, 0.9);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.content-info {
  padding: 20px;
}

.content-info h3 {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 10px;
  line-height: 1.4;
}

.content-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.content-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #999;
  margin-bottom: 12px;
}

.content-stats {
  text-align: right;
}

.content-stats .likes {
  color: #e74c3c;
  font-weight: 500;
}

/* 加载和空状态 */
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

  .content-grid {
    grid-template-columns: 1fr;
  }

  .content-info {
    padding: 15px;
  }
}
</style>
