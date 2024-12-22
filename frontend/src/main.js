// frontend/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersist from 'pinia-plugin-persist'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import './assets/css/input.css'
import { showToast } from '@/components/ToastMessage'
import store from './store'
// axios 配置
axios.defaults.headers.common['Content-Type'] = 'application/json'

// 添加请求拦截器
axios.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// 添加响应拦截器
axios.interceptors.response.use(
    response => response,
    error => {
        if (error.response) {
            if (error.response.status === 401) {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                showToast('登录已过期，请重新登录', 'warning')
                router.push('/login')
            }
        }
        return Promise.reject(error)
    }
)

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersist)
app.use(store)
app.use(pinia)
app.use(router)
app.config.globalProperties.$axios = axios

// 添加全局 Toast 方法
app.config.globalProperties.$toast = showToast

app.mount('#app')