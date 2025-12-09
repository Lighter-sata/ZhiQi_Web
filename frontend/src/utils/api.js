/**
 * 芝栖养生平台 - API工具函数
 * 提供统一的HTTP请求封装和错误处理
 */

import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 添加认证token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 添加请求时间戳（防止缓存）
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }

    return config
  },
  error => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    const { data } = response

    // 处理业务错误
    if (data && data.msg && data.msg.includes('错误')) {
      console.warn('业务错误:', data.msg)
    }

    return response
  },
  error => {
    const { response, request, message } = error

    if (response) {
      // 服务器响应错误
      const { status, data } = response

      switch (status) {
        case 400:
          console.error('请求参数错误:', data.msg || 'Bad Request')
          break
        case 401:
          console.error('未授权访问:', data.msg || 'Unauthorized')
          // 清除本地token并跳转登录
          localStorage.removeItem('access_token')
          localStorage.removeItem('user')
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
          break
        case 403:
          console.error('权限不足:', data.msg || 'Forbidden')
          break
        case 404:
          console.error('资源不存在:', data.msg || 'Not Found')
          break
        case 500:
          console.error('服务器内部错误:', data.msg || 'Internal Server Error')
          break
        default:
          console.error(`HTTP ${status} 错误:`, data.msg || 'Unknown Error')
      }
    } else if (request) {
      // 网络错误
      console.error('网络错误: 请检查网络连接')
    } else {
      // 其他错误
      console.error('请求错误:', message)
    }

    return Promise.reject(error)
  }
)

// API接口定义
export const api = {
  // 用户认证
  auth: {
    register: (data) => apiClient.post('/api/auth/register', data),
    login: (data) => apiClient.post('/api/auth/login', data),
    getProfile: () => apiClient.get('/api/auth/profile'),
    updateProfile: (data) => apiClient.put('/api/auth/profile', data)
  },

  // 内容管理
  content: {
    getList: (params) => apiClient.get('/api/content/', { params }),
    getDetail: (id) => apiClient.get(`/api/content/${id}`),
    create: (data) => apiClient.post('/api/content/', data),
    update: (id, data) => apiClient.put(`/api/content/${id}`, data),
    delete: (id) => apiClient.delete(`/api/content/${id}`),
    like: (id) => apiClient.post(`/api/content/${id}/like`)
  },

  // 产品管理
  products: {
    getList: (params) => apiClient.get('/api/products/', { params }),
    getDetail: (id) => apiClient.get(`/api/products/${id}`)
  },

  // 活动管理
  activities: {
    getList: (params) => apiClient.get('/api/activities/', { params }),
    getDetail: (id) => apiClient.get(`/api/activities/${id}`),
    create: (data) => apiClient.post('/api/activities/', data),
    register: (id) => apiClient.post(`/api/activities/${id}/register`)
  },

  // 体验基地
  bases: {
    getList: () => apiClient.get('/api/bases/'),
    getDetail: (id) => apiClient.get(`/api/bases/${id}`)
  },

  // 订单管理
  orders: {
    getList: (params) => apiClient.get('/api/orders/', { params }),
    getDetail: (id) => apiClient.get(`/api/orders/${id}`),
    create: (data) => apiClient.post('/api/orders/', data)
  },

  // 支付
  payments: {
    createPayment: (data) => apiClient.post('/api/payments/create-payment', data)
  },

  // 评论
  reviews: {
    getList: (params) => apiClient.get('/api/reviews/', { params }),
    create: (data) => apiClient.post('/api/reviews/', data)
  },

  // 用户中心
  user: {
    getDashboard: () => apiClient.get('/api/user/dashboard'),
    getFavorites: (params) => apiClient.get('/api/user/favorites', { params }),
    addFavorite: (data) => apiClient.post('/api/user/favorites', data),
    removeFavorite: (id) => apiClient.delete(`/api/user/favorites/${id}`)
  },

  // 后台管理
  admin: {
    getStats: () => apiClient.get('/api/admin/stats'),
    getActivitiesReview: () => apiClient.get('/api/admin/activities/review'),
    reviewActivity: (id, data) => apiClient.put(`/api/admin/activities/${id}/review`, data),
    getContentReview: () => apiClient.get('/api/admin/content/review'),
    publishContent: (id) => apiClient.put(`/api/admin/content/${id}/publish`)
  },

  // 文件上传
  upload: {
    file: (file, onProgress) => {
      const formData = new FormData()
      formData.append('file', file)

      return apiClient.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: onProgress
      })
    }
  }
}

// 导出默认实例
export default apiClient

// 工具函数
export const handleApiError = (error, defaultMessage = '操作失败，请重试') => {
  if (error.response) {
    const { data } = error.response
    return data.msg || defaultMessage
  } else if (error.request) {
    return '网络连接失败，请检查网络设置'
  } else {
    return error.message || defaultMessage
  }
}

export const isAuthError = (error) => {
  return error.response && error.response.status === 401
}

export const isNetworkError = (error) => {
  return !error.response && error.request
}
