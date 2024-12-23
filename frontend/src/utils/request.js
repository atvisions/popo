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
const API_PATHS = {
  // 认证相关
  AUTH: {
    SEND_SMS: `/v1/auth/sms/send/`,
    REGISTER: `/v1/auth/register/`,
    PASSWORD_LOGIN: `/v1/auth/login/password/`,
    CODE_LOGIN: `/v1/auth/login/code/`,
    LOGOUT: `/v1/auth/logout/`,
    RESET_PASSWORD: `/v1/auth/password/reset/`,
    REFRESH_TOKEN: `/v1/auth/token/refresh/`,
  },
  
  // 用户资料相关
  USERS: {
    PROFILE: '/v1/users/profile/',
    AVATAR: '/v1/users/profile/avatar/'
  },
  
  // 账户管理相关
  ACCOUNT: {
    CHANGE_PASSWORD: `/v1/users/account/password/`,
    CHANGE_PHONE: `/v1/users/account/phone/`,
    DELETE_ACCOUNT: `/v1/users/account/delete/`,
  }
}

// 创建请求实例
const request = axios.create(BASE_CONFIG)
const publicRequest = axios.create(BASE_CONFIG)

// Token 刷新控制
let isRefreshing = false
let refreshSubscribers = []

const addRefreshSubscriber = (callback) => {
  refreshSubscribers.push(callback)
}

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
    return response
  },
  async error => {
    const originalRequest = error.config

    // 处理黑名单错误
    if (error.response?.data?.detail?.includes('blacklist')) {
      await store.dispatch('handleTokenExpired')
      return Promise.reject(new Error('登录已过期，请重新登录'))
    }

    // 处理刷新token失败
    if (originalRequest.url === API_PATHS.AUTH.REFRESH_TOKEN) {
      await store.dispatch('handleTokenExpired')
      return Promise.reject(error)
    }

    // 处理401错误
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
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
        onRefreshed(newToken)
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return request(originalRequest)
      } catch (refreshError) {
        await store.dispatch('handleTokenExpired')
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

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

export { API_PATHS }
export { request as default, publicRequest }