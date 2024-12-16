import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ProView from '../views/ProView.vue'
import FAQView from '../views/FAQView.vue'
import CareerNewsView from '../views/CareerNewsView.vue'
import ResumeTemplateView from '../views/ResumeTemplateView.vue'
// 定义路由配置
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      guest: true
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      guest: true
    }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: {
      guest: true
    }
  },
  {
    path: '/pro',
    name: 'pro',
    component: ProView,
  },
  {
    path: '/faq',
    name: 'faq',
    component: FAQView,
  },
  {
    path: '/news',
    name: 'news',
    component: CareerNewsView,
  },
  {
    path: '/templates',
    name: 'templates',
    component: ResumeTemplateView,
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory('/'),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  
  // 检查页面是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  // 检查页面是否是游客页面（登录、注册等）
  const isGuestPage = to.matched.some(record => record.meta.guest)

  if (requiresAuth && !token) {
    // 需要认证但没有 token，重定向到登录页
    next({ name: 'login' })
  } else if (token && isGuestPage) {
    // 已登录但访问游客页面，重定向到首页
    next({ name: 'home' })
  } else {
    // 其他情况正常通过
    next()
  }
})

export default router
