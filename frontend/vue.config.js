const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  // 开发服务器配置
  devServer: {
    port: process.env.VUE_APP_PORT || 8080,
    host: '0.0.0.0',
    // 代理API请求到后端服务
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      },
      // 文件上传代理
      '/uploads': {
        target: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000',
        changeOrigin: true
      }
    },
    // 自动打开浏览器
    open: process.env.NODE_ENV === 'development',
    // HTTPS配置（开发环境可选）
    https: false,
    // 热重载
    hot: true,
    // 错误覆盖层
    overlay: {
      warnings: true,
      errors: true
    }
  },

  // 构建配置
  configureWebpack: {
    // 代码分割优化
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          // 第三方库
          vendor: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          // Vue相关库
          vue: {
            name: 'chunk-vue',
            test: /[\\/]node_modules[\\/]vue[\\/]/,
            priority: 20,
            chunks: 'initial'
          },
          // UI组件库（如果使用的话）
          ui: {
            name: 'chunk-ui',
            test: /[\\/]node_modules[\\/](element-plus|ant-design-vue)[\\/]/,
            priority: 15,
            chunks: 'initial'
          }
        }
      }
    },

    // 性能优化
    performance: {
      // 生产环境性能提示
      hints: process.env.NODE_ENV === 'production' ? 'warning' : false,
      // 资源大小限制
      maxAssetSize: 1024 * 1024, // 1MB
      maxEntrypointSize: 1024 * 1024 // 1MB
    }
  },

  // 路径别名配置
  chainWebpack: config => {
    // 添加路径别名
    config.resolve.alias
      .set('@', path.resolve(__dirname, 'src'))
      .set('@components', path.resolve(__dirname, 'src/components'))
      .set('@views', path.resolve(__dirname, 'src/views'))
      .set('@utils', path.resolve(__dirname, 'src/utils'))
      .set('@assets', path.resolve(__dirname, 'src/assets'))

    // 生产环境优化
    if (process.env.NODE_ENV === 'production') {
      // 移除console.log
      config.optimization.minimizer('terser').tap(args => {
        args[0].terserOptions.compress.drop_console = true
        args[0].terserOptions.compress.drop_debugger = true
        return args
      })

      // Gzip压缩
      config.plugin('compression').use(require('compression-webpack-plugin'), [{
        algorithm: 'gzip',
        test: /\.(js|css|html|svg)$/,
        threshold: 10240, // 10KB以上文件压缩
        minRatio: 0.8
      }])
    }
  },

  // CSS配置
  css: {
    // 是否将组件内的 CSS 提取到单独的文件
    extract: process.env.NODE_ENV === 'production',
    // CSS源映射
    sourceMap: process.env.NODE_ENV === 'development',
    // 全局样式导入
    loaderOptions: {
      scss: {
        additionalData: `
          @import "~@/styles/variables.scss";
          @import "~@/styles/mixins.scss";
        `
      }
    }
  },

  // PWA配置（可选）
  pwa: {
    name: '芝栖养生平台',
    shortName: '芝栖养生',
    description: '专业灵芝养生健康平台，连接自然之力，引领品质生活',
    themeColor: '#8b5a3c',
    backgroundColor: '#ffffff',
    display: 'standalone',
    startUrl: '/',
    icons: [
      {
        src: '/img/icons/icon-192x192.png',
        sizes: '192x192',
        type: 'image/png'
      },
      {
        src: '/img/icons/icon-512x512.png',
        sizes: '512x512',
        type: 'image/png'
      }
    ],
    // 工作框配置
    workboxOptions: {
      skipWaiting: true,
      clientsClaim: true,
      // 缓存策略
      runtimeCaching: [
        {
          urlPattern: /\/api\//,
          handler: 'NetworkFirst',
          options: {
            networkTimeoutSeconds: 10,
            cacheName: 'api-cache',
            expiration: {
              maxEntries: 100,
              maxAgeSeconds: 60 * 60 * 24 // 24小时
            }
          }
        },
        {
          urlPattern: /\.(?:png|jpg|jpeg|svg|gif)$/,
          handler: 'CacheFirst',
          options: {
            cacheName: 'image-cache',
            expiration: {
              maxEntries: 200,
              maxAgeSeconds: 60 * 60 * 24 * 30 // 30天
            }
          }
        }
      ]
    }
  },

  // 国际化配置（可选）
  pluginOptions: {
    i18n: {
      locale: 'zh-CN',
      fallbackLocale: 'zh-CN',
      localeDir: 'locales',
      enableInSFC: false
    }
  },

  // 构建输出配置
  outputDir: 'dist',
  assetsDir: 'assets',
  publicPath: process.env.NODE_ENV === 'production'
    ? process.env.VUE_APP_PUBLIC_PATH || '/'
    : '/',

  // 生产环境配置
  productionSourceMap: false,
  lintOnSave: process.env.NODE_ENV === 'development',

  // 开发环境配置
  configureWebpack: process.env.NODE_ENV === 'development' ? {
    devtool: 'cheap-module-eval-source-map'
  } : {}
})

// 路径模块（用于别名配置）
const path = require('path')
