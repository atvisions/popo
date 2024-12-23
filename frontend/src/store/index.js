import { createStore } from 'vuex'
import { getUserInfo } from '@/api/user' 
import { publicRequest } from '@/utils/request'
import router from '@/router'
import { showToast } from '@/components/ToastMessage'

// Token 相关常量
const TOKEN_CONFIG = {
  // 有效期配置
  NORMAL_EXPIRATION_TIME: 7200 * 1000, // 普通登录时token有效期2小时
  REMEMBER_EXPIRATION_TIME: 7 * 24 * 3600 * 1000, // 记住我时token有效期7天
  REFRESH_INTERVAL: 20 * 60 * 1000, // 刷新间隔20分钟
  REFRESH_THRESHOLD: 30 * 60 * 1000, // 刷新阈值30分钟
  
  // 存储键名配置
  STORAGE_KEYS: {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    EXPIRATION: 'token_expiration',
    REMEMBER_ME: 'remember_me'
  }
}

let refreshInterval = null
let isRefreshingToken = false
let refreshSubscribers = []

// Token 刷新订阅机制
const addRefreshSubscriber = (callback) => {
  refreshSubscribers.push(callback)
}

const onTokenRefreshed = (token) => {
  refreshSubscribers.forEach(callback => callback(token))
  refreshSubscribers = []
}

/**
 * 短信验证码场景枚举
 * @enum {string}
 */
export const SMS_SCENE = {
  REGISTER: 'register',
  LOGIN: 'login',
  RESET_PASSWORD: 'reset_password',
  CHANGE_PHONE: 'change_phone'
}

/**
 * Vuex Store 配置
 * @type {import('vuex').StoreOptions}
 */
export default createStore({
  state: {
    userInfo: null,
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
    tokenExpiration: null,
    userPhone: null,
    userId: null,
    userAvatar: null,
    rememberMe: false,
    isHandlingExpiration: false
  },

  getters: {
    getFullMediaUrl: () => (path) => {
      if (!path) return '/default-avatar.png'
      if (path.startsWith('http')) return path
      return `${import.meta.env.VITE_API_URL}${path}`
    },
    getUserInfo: state => state.userInfo,
    isAuthenticated: state => state.isAuthenticated,
    getAccessToken: state => state.accessToken,
    getUserPhone: state => state.userPhone,
    getUserId: state => state.userId,
    getUserAvatar: (state, getters) => {
      const profileAvatar = state.userInfo?.data?.avatar
      const storedAvatar = localStorage.getItem('user_avatar') || sessionStorage.getItem('user_avatar')
      const avatarPath = profileAvatar || storedAvatar || state.userAvatar
      return getters.getFullMediaUrl(avatarPath)
    },
    wechatLoginStatus: state => state.wechatLoginStatus,
    wechatLoginError: state => state.wechatLoginError
  },

  mutations: {
    SET_AUTH_DATA(state, { tokens, user, remember, phone }) {
      if (tokens) {
        // 根据记住我选项设置过期时间
        const expiration = remember ? 
        Date.now() + TOKEN_CONFIG.REMEMBER_EXPIRATION_TIME :
        Date.now() + TOKEN_CONFIG.NORMAL_EXPIRATION_TIME
        // 更新 state
        state.accessToken = tokens.access
        state.refreshToken = tokens.refresh
        state.tokenExpiration = expiration
        state.isAuthenticated = true
        state.rememberMe = remember
    
        // 更新 localStorage
        const { STORAGE_KEYS } = TOKEN_CONFIG
        localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.access)
        localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh)
        localStorage.setItem(STORAGE_KEYS.EXPIRATION, expiration.toString())
        localStorage.setItem(STORAGE_KEYS.REMEMBER_ME, remember.toString())
    
        // 调试日志
        if (process.env.NODE_ENV === 'development') {
          console.log('Auth data updated:', {
            current: new Date().toLocaleString(),
            expiration: new Date(expiration).toLocaleString(),
            timeLeft: Math.round((expiration - Date.now()) / 1000 / 60) + ' minutes',
            remember: remember
          })
        }
      }

      if (phone) {
        state.userPhone = phone
        localStorage.setItem('account_phone', phone)
      } else {
        const savedPhone = localStorage.getItem('account_phone')
        if (savedPhone) {
          state.userPhone = savedPhone
        }
      }

      if (user) {
        state.userInfo = {
          ...user,
          accountPhone: phone || state.userPhone,
          profile: user.profile || {}
        }
        state.userId = user.id

        if (user.profile?.avatar) {
          state.userAvatar = user.profile.avatar
          const storage = remember ? localStorage : sessionStorage
          storage.setItem('user_avatar', user.profile.avatar)
        }

        const storage = remember ? localStorage : sessionStorage
        storage.setItem('user_id', user.id.toString())
      }

      state.rememberMe = remember
      localStorage.setItem('remember_me', remember.toString())
    },

    SET_USER_INFO(state, userInfo) {
      // 保存原有的手机号
      const accountPhone = state.userPhone
      
      // 处理可能的不同数据结构
      const userData = userInfo.data || userInfo
      const profile = userData.profile || {}
      const avatar = userData.avatar || profile.avatar
      
      // 更新状态
      state.userInfo = {
        ...state.userInfo,
        ...userData,
        accountPhone,
        profile: {
          ...(state.userInfo?.profile || {}),
          ...profile,
          avatar  // 确保头像信息被正确保存
        }
      }
      
      // 更新用户 ID
      if (userData.id) {
        state.userId = userData.id
      }
      
      // 更新头像
      if (avatar) {
        state.userAvatar = avatar
        // 根据记住我选项决定存储位置
        const storage = state.rememberMe ? localStorage : sessionStorage
        storage.setItem('user_avatar', avatar)
      }
    },

    CLEAR_AUTH(state) {
      // 清除状态
      state.userInfo = null
      state.isAuthenticated = false
      state.accessToken = null
      state.refreshToken = null
      state.tokenExpiration = null
      state.userPhone = null
      state.userId = null
      state.userAvatar = null
      state.rememberMe = false

      // 清除定时器
      if (refreshInterval) {
        clearInterval(refreshInterval)
        refreshInterval = null
      }

      // 清除 TOKEN_CONFIG 中定义的存储项
      const { STORAGE_KEYS } = TOKEN_CONFIG
      Object.values(STORAGE_KEYS).forEach(key => {
        localStorage.removeItem(key)
      })

      // 清除其他相关存储项
      const additionalKeys = [
        'account_phone',
        'redirectPath',
        'user_id',
        'user_avatar'
      ]

      // 从 localStorage 和 sessionStorage 都清除
      additionalKeys.forEach(key => {
        localStorage.removeItem(key)
        sessionStorage.removeItem(key)
      })

      if (process.env.NODE_ENV === 'development') {
        console.log('Auth state and storage cleared completely')
      }
    }
  },
  actions: {
    async checkAuth({ dispatch, commit }) {
      try {
        const { STORAGE_KEYS } = TOKEN_CONFIG
        const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)
        const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)
        const expiration = localStorage.getItem(STORAGE_KEYS.EXPIRATION)
        const rememberMe = localStorage.getItem(STORAGE_KEYS.REMEMBER_ME) === 'true'

        if (!token || !refreshToken || !expiration) {
          console.log('Missing auth data:', { token: !!token, refreshToken: !!refreshToken, expiration: !!expiration })
          commit('CLEAR_AUTH')
          return false
        }
    
        const now = new Date().getTime()
        const expirationTime = parseInt(expiration)
    
        // 调试日志
        if (process.env.NODE_ENV === 'development') {
          console.log('Token Status:', {
            currentTime: new Date(now).toLocaleString(),
            expirationTime: new Date(expirationTime).toLocaleString(),
            timeLeft: Math.round((expirationTime - now) / 1000 / 60) + ' minutes'
          })
        }
    
        // 每次页面刷新时都刷新 token
        try {
          console.log('Refreshing token on page load...')
          await dispatch('refreshToken')
          return true
        } catch (error) {
          console.error('Token refresh failed:', error)
          // 如果刷新失败，尝试使用现有的 token
          if (now < expirationTime) {
            commit('SET_AUTH_DATA', {
              tokens: {
                access: token,
                refresh: refreshToken
              },
              expirationTime,
              remember: rememberMe,
              phone: localStorage.getItem('account_phone')
            })
    
            const userInfo = await dispatch('fetchUserInfo')
            if (userInfo) {
              commit('SET_USER_INFO', userInfo)
              return true
            }
          }
          
          commit('CLEAR_AUTH')
          return false
        }
      } catch (error) {
        console.error('Check auth error:', error)
        commit('CLEAR_AUTH')
        return false
      }
    },

    async initAuth({ commit, dispatch }) {
      try {
        // 清除可能存在的旧定时器
        if (refreshInterval) {
          clearInterval(refreshInterval)
          refreshInterval = null
        }
    
        const result = await dispatch('checkAuth')
        
        if (result) {
          // 设置新的定时器
          refreshInterval = setInterval(async () => {
            if (process.env.NODE_ENV === 'development') {
              console.log('Scheduled token check running...')
            }
            await dispatch('checkAuth')
          }, TOKEN_CONFIG.REFRESH_INTERVAL)
    
          if (process.env.NODE_ENV === 'development') {
            console.log('Token check interval set:', TOKEN_CONFIG.REFRESH_INTERVAL / 1000, 'seconds')
          }
        }
        
        return result
      } catch (error) {
        console.error('Init auth error:', error)
        commit('CLEAR_AUTH')
        return false
      }
    },

    async fetchUserInfo({ commit }) {
      const response = await getUserInfo()
      if (!response.data) {
        throw new Error('获取用户信息失败：无数据返回')
      }
      
      const userInfo = {
        ...response.data,
        profile: {
          ...response.data.profile,
          avatar: response.data.data?.avatar || response.data.profile?.avatar
        }
      }
      
      commit('SET_USER_INFO', userInfo)
      return userInfo
    },

    async loginWithPassword({ commit, dispatch }, { credentials, remember }) {
      try {
        const response = await publicRequest({
          url: '/v1/auth/login/password/',
          method: 'post',
          data: {
            phone: credentials.phone,
            password: credentials.password
          }
        })
    
        const { code, message, data } = response.data
        if (code !== 200 || !data) {
          throw new Error(message || '登录失败')
        }
    
        // 保存认证信息
        commit('SET_AUTH_DATA', {
          tokens: data.tokens,
          user: data.user,
          remember,
          phone: credentials.phone
        })
    
        // 立即获取完整的用户信息
        try {
          const userInfo = await dispatch('fetchUserInfo')
          if (userInfo) {
            commit('SET_USER_INFO', userInfo)
          }
        } catch (error) {
          console.error('获取用户完整信息失败：', error)
        }
    
        return data
      } catch (error) {
        commit('CLEAR_AUTH')
        throw error
      }
    },

    async refreshToken({ commit, state }) {
      if (isRefreshingToken) {
        return new Promise((resolve) => {
          addRefreshSubscriber(token => {
            resolve(token)
          })
        })
      }
    
      try {
        isRefreshingToken = true
        const refreshToken = state.refreshToken || localStorage.getItem('refresh_token')
        
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }
    
        const response = await publicRequest({
          url: '/v1/auth/token/refresh/',
          method: 'post',
          data: { refresh: refreshToken }
        })
    
        if (!response.data?.access || response.data?.code !== 200) {
          throw new Error(response.data?.message || 'Invalid refresh response')
        }
    
        const newExpirationTime = new Date().getTime() + (
          state.rememberMe ? 
          TOKEN_CONFIG.REMEMBER_EXPIRATION_TIME : 
          TOKEN_CONFIG.NORMAL_EXPIRATION_TIME
        )
    
        // 立即更新 state 和 localStorage 中的 tokens
        commit('SET_AUTH_DATA', {
          tokens: {
            access: response.data.access,
            refresh: response.data.refresh  // 使用新的 refresh token
          },
          expirationTime: newExpirationTime,
          remember: state.rememberMe
        })
    
        onTokenRefreshed(response.data.access)
        return response.data.access
    
      } catch (error) {
        console.error('Token refresh failed:', error.response?.data || error.message)
        
        if (error.response?.data?.detail?.includes('黑名单') || 
            error.response?.status === 400) {
          await this.dispatch('handleTokenExpired')
        } else {
          commit('CLEAR_AUTH')
        }
        throw error
      } finally {
        isRefreshingToken = false
      }
    },
    async logout({ commit, state }) {
      try {
        const refreshToken = state.refreshToken || localStorage.getItem('refresh_token')
        
        if (refreshToken) {
          try {
            await publicRequest({
              url: '/v1/auth/logout/',
              method: 'post',
              headers: {
                'Authorization': `Bearer ${state.accessToken || localStorage.getItem('access_token')}`
              },
              data: { 
                refresh: refreshToken 
              }
            })
            console.log('Logout successful')
          } catch (error) {
            console.error('Logout API error:', error)
          }
        }
      } finally {
        commit('CLEAR_AUTH')
        router.push('/login')
      }
    },

    async loginWithToken({ commit, dispatch }, token) {
      try {
        const expirationTime = new Date().getTime() + TOKEN_CONFIG.EXPIRATION_TIME
        
        commit('SET_AUTH_DATA', {
          tokens: { access: token },
          expirationTime,
          remember: false
        })
        
        await dispatch('fetchUserInfo')
        return true
      } catch (error) {
        commit('CLEAR_AUTH')
        throw error
      }
    },
    
    async handleTokenExpired({ commit, state }) {
      if (state.isHandlingExpiration) {
        return
      }
      
      state.isHandlingExpiration = true
      
      try {
        const currentPath = router.currentRoute.value.fullPath
        const isLoginPage = currentPath === '/login'

        // 先清除认证信息
        commit('CLEAR_AUTH')
        
        // 保存重定向路径（如果不是登录页）
        if (!isLoginPage) {
          localStorage.setItem('redirectPath', currentPath)
          showToast('登录已过期，请重新登录', 'warning')
          
          await router.push({
            path: '/login',
            query: { 
              redirect: currentPath,
              source: 'expired'
            }
          })
        }
      } catch (error) {
        console.error('Error during token expiration handling:', error)
      } finally {
        state.isHandlingExpiration = false
      }
    }
  }
})