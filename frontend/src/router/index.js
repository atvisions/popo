import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ResumeTemplateView from '../views/ResumeTemplateView.vue'
import CareerNewsView from '../views/CareerNewsView.vue'
import FAQView from '../views/FAQView.vue'
import ProView from '../views/ProView.vue'
const router = createRouter({
  history: createWebHistory(''),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { requiresGuest: true }
    },
    {
      path: '/templates',
      name: 'templates',
      component: ResumeTemplateView
    },
    {
      path: '/news',
      name: 'news',
      component: CareerNewsView
    },
    {
      path: '/faq',
      name: 'faq',
      component: FAQView
    },
    {
      path: '/pro',
      name: 'pro',
      component: ProView
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: ResetPasswordView,
      meta: { requiresGuest: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token')
  
  if (to.meta.requiresGuest && isLoggedIn) {
    next('/')
    return
  }
  
  next()
})

export default router
