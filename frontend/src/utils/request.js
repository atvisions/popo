import axios from 'axios'
import store from '@/store'
import { showToast } from '@/components/ToastMessage'

// 基础配置
const BASE_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://192.168.3.16:8000',
  timeout: 5000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
}

// API 版本和路径配置
const API_VERSION = 'v1'
const API_PATHS = {
  REFRESH_TOKEN: `/${API_VERSION}/auth/token/refresh/`,
  AUTH_PREFIX: `/${API_VERSION}/auth/`,
  USERS_PREFIX: `/${API_VERSION}/users/`
}

// 创建请求实例
const request = axios.create(BASE_CONFIG)
const publicRequest = axios.create(BASE_CONFIG)

// Token 刷新控制
let isRefreshing = false
let refreshSubscribers = []

// 添加刷新订阅
const addRefreshSubscriber = (callback) => {
  refreshSubscribers.push(callback)
}

// 执行订阅回调
const onRefreshed = (token) => {
  refreshSubscribers.forEach(callback => callback(token))
  refreshSubscribers = []
}

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = store.getters.getAccessToken || localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 调试日志
    if (process.env.NODE_ENV === 'development') {
      console.log('Request:', {
        url: config.url,
        method: config.method,
        headers: config.headers
      })
    }
    
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    if (process.env.NODE_ENV === 'development') {
      console.log('Response:', {
        url: response.config.url,
        status: response.status,
        data: response.data
      })
    }
    return response
  },
  async error => {
    if (import.meta.env.DEV) {
      console.error('Response Error:', {
        url: error.config?.url,
        status: error.response?.status,
        data: error.response?.data
      })
    }

    const originalRequest = error.config

    // 处理黑名单错误
    if (error.response?.data?.detail?.includes('blacklist')) {
      await store.dispatch('handleTokenExpired')
      return Promise.reject(new Error('登录已过期，请重新登录'))
    }

    // 处理刷新token失败
    if (originalRequest.url === API_PATHS.REFRESH_TOKEN) {
      await store.dispatch('handleTokenExpired')
      return Promise.reject(error)
    }

    // 处理401错误
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // 等待token刷新完成
        return new Promise(resolve => {
          addRefreshSubscriber(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(request(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true
      
      try {
        await store.dispatch('refreshToken')
        const newToken = store.getters.getAccessToken
        
        // 通知所有等待的请求
        onRefreshed(newToken)
        
        // 重试当前请求
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return request(originalRequest)
      } catch (refreshError) {
        await store.dispatch('handleTokenExpired')
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    // 错误提示
    handleErrorMessage(error)

    return Promise.reject(error)
  }
)

// 公开请求的响应拦截器
publicRequest.interceptors.response.use(
  response => response,
  error => {
    handleErrorMessage(error)
    return Promise.reject(error)
  }
)

// 统一的错误消息处理
const handleErrorMessage = (error) => {
  if (error.response?.data) {
    const { message, detail, errors } = error.response.data
    
    if (errors) {
      // 处理字段错误
      const errorMessages = Object.values(errors)
        .flat()
        .filter(msg => msg)
        .join(', ')
      if (errorMessages) {
        showToast(errorMessages, 'error')
        return
      }
    }
    
    if (message) {
      showToast(message, 'error')
    } else if (detail) {
      showToast(detail, 'error')
    } else {
      showToast('请求失败，请重试', 'error')
    }
  } else if (error.request) {
    showToast('网络连接失败，请检查网络', 'error')
  } else {
    showToast('请求发送失败', 'error')
  }
}

// 导出 API 路径配置
export { API_PATHS }
export { request as default, publicRequest }