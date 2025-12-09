<template>
  <div class="home">
    <!-- 品牌Hero区域 -->
    <section class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">
            <span class="brand-highlight">芝栖养生</span>
            <br>
            让健康成为生活方式
          </h1>
          <p class="hero-subtitle">
            专业灵芝养生健康平台，连接自然之力，引领品质生活
          </p>
          <div class="hero-actions">
            <router-link to="/products" class="btn btn-primary btn-lg">
              探索产品
            </router-link>
            <router-link to="/activities" class="btn btn-outline btn-lg">
              体验活动
            </router-link>
          </div>
        </div>
        <div class="hero-visual">
          <div class="hero-image">
            <img src="https://via.placeholder.com/500x400/8b5a3c/ffffff?text=灵芝养生" alt="灵芝养生">
          </div>
        </div>
      </div>
    </section>

    <!-- 核心功能模块 -->
    <section class="features-section">
      <div class="container">
        <div class="section-header">
          <h2>我们的服务</h2>
          <p>三大核心模块，满足您的全方位养生需求</p>
        </div>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <span class="icon-content">📚</span>
            </div>
            <h3>内容中心</h3>
            <p>硬核科普文章、生活方式内容、品牌文化展示，让您深入了解灵芝养生之道</p>
            <router-link to="/content" class="feature-link">查看内容 →</router-link>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <span class="icon-product">🛍️</span>
            </div>
            <h3>养生产品</h3>
            <p>甄选灵芝片、七味茶包、孢子粉等优质产品，支持溯源查询，安全放心</p>
            <router-link to="/products" class="feature-link">选购产品 →</router-link>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <span class="icon-activity">🎯</span>
            </div>
            <h3>体验活动</h3>
            <p>90分钟灵芝采摘课、瑜伽工作坊、手作体验，多种活动等您参与</p>
            <router-link to="/activities" class="feature-link">参与活动 →</router-link>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <span class="icon-base">🏞️</span>
            </div>
            <h3>体验基地</h3>
            <p>静心一夜住宿体验、工坊周末活动，沉浸式养生度假基地</p>
            <router-link to="/bases" class="feature-link">了解基地 →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 品牌承诺 -->
    <section class="promise-section">
      <div class="container">
        <div class="promise-content">
          <h2>我们的承诺</h2>
          <div class="promise-grid">
            <div class="promise-item">
              <div class="promise-icon">🌿</div>
              <h4>天然品质</h4>
              <p>选用优质野生灵芝，严格把控生长环境，确保产品纯天然无污染</p>
            </div>
            <div class="promise-item">
              <div class="promise-icon">🔬</div>
              <h4>科学配方</h4>
              <p>结合现代科技与传统养生智慧，科学提取有效成分</p>
            </div>
            <div class="promise-item">
              <div class="promise-icon">📋</div>
              <h4>品质溯源</h4>
              <p>每件产品配备专属溯源码，可追溯种植、加工、检测全过程</p>
            </div>
            <div class="promise-item">
              <div class="promise-icon">💝</div>
              <h4>专业服务</h4>
              <p>提供专业的养生咨询和指导，让健康成为一种生活方式</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
};
</script>

<style scoped>
/* Hero区域样式 */
.hero-section {
  background: linear-gradient(135deg, #8b5a3c 0%, #a67c52 50%, #b89a6a 100%);
  color: white;
  padding: 80px 0;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.1;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-content {
  z-index: 2;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 20px;
}

.brand-highlight {
  color: #ffd700;
  position: relative;
}

.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 20px;
}

.hero-visual {
  text-align: center;
}

.hero-image {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.hero-image img {
  width: 100%;
  height: auto;
  display: block;
}

/* 功能模块样式 */
.features-section {
  padding: 80px 0;
  background: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-header h2 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 15px;
  position: relative;
}

.section-header h2::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #8b5a3c, #a67c52);
  border-radius: 2px;
}

.section-header p {
  font-size: 1.1rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 40px;
}

.feature-card {
  background: white;
  border-radius: 16px;
  padding: 40px 30px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(139, 90, 60, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(139, 90, 60, 0.15);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #8b5a3c, #a67c52);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  font-size: 2rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 15px;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.feature-link {
  color: #8b5a3c;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.feature-link:hover {
  color: #a67c52;
}

/* 承诺区域样式 */
.promise-section {
  padding: 80px 0;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.promise-content {
  text-align: center;
}

.promise-content h2 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 60px;
  position: relative;
}

.promise-content h2::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #8b5a3c, #a67c52);
  border-radius: 2px;
}

.promise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
}

.promise-item {
  background: white;
  border-radius: 16px;
  padding: 40px 30px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(139, 90, 60, 0.1);
  transition: all 0.3s ease;
}

.promise-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(139, 90, 60, 0.15);
}

.promise-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.promise-item h4 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 15px;
}

.promise-item p {
  color: #666;
  line-height: 1.6;
}

/* 按钮样式 */
.btn {
  display: inline-block;
  padding: 12px 24px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #8b5a3c, #a67c52);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #a67c52, #b89a6a);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(139, 90, 60, 0.3);
}

.btn-outline {
  background: transparent;
  color: #8b5a3c;
  border: 2px solid #8b5a3c;
}

.btn-outline:hover {
  background: #8b5a3c;
  color: white;
  transform: translateY(-2px);
}

.btn-lg {
  padding: 16px 32px;
  font-size: 1.1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-actions {
    justify-content: center;
  }

  .features-grid,
  .promise-grid {
    grid-template-columns: 1fr;
  }

  .features-section,
  .promise-section {
    padding: 60px 0;
  }

  .section-header h2 {
    font-size: 2rem;
  }
}
</style>