import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersist from 'pinia-plugin-persist'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import './assets/css/input.css'
import { showToast } from '@/components/ToastMessage'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

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

// 创建应用实例
const app = createApp(App)

// 创建 Pinia 实例
const pinia = createPinia()
pinia.use(piniaPluginPersist)

// 按顺序使用插件
app.use(ElementPlus)  // 移到这里
app.use(store)
app.use(pinia)
app.use(router)

// 配置全局属性
app.config.globalProperties.$axios = axios
app.config.globalProperties.$toast = showToast

// 最后挂载
app.mount('#app')