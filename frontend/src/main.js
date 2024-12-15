// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import './assets/css/input.css'

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
                router.push('/login')
            }
        }
        return Promise.reject(error)
    }
)

const app = createApp(App)
app.use(router)
app.config.globalProperties.$axios = axios
app.mount('#app')