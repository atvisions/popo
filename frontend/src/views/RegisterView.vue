<template>
  <HeadView />
  <div class="min-h-screen bg-gray-50 pt-14">
    <div class="sm:mx-auto sm:w-full sm:max-w-md pt-8">
      <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">注册账号</h2>
    </div>
    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
      <div class="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <!-- 手机号输入 -->
          <div>
            <label for="phone" class="block text-sm font-medium leading-6 text-gray-900">手机号</label>
            <div class="mt-2">
              <input 
                id="phone" 
                v-model="form.phone" 
                type="text" 
                required
                placeholder="请输入手机号"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
              />
            </div>
          </div>

          <!-- 验证码输入 -->
          <div>
            <label for="code" class="block text-sm font-medium leading-6 text-gray-900">验证码</label>
            <div class="mt-2 flex">
              <div class="flex-grow">
                <input 
                  id="code" 
                  v-model="form.code" 
                  type="text" 
                  required
                  placeholder="请输入验证码"
                  class="block w-full rounded-l-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
                />
              </div>
              <button 
                type="button"
                @click="getVerifyCode"
                :disabled="form.countdown > 0 || sendingCode"
                class="relative -ml-px inline-flex items-center rounded-r-md px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10"
                :class="form.countdown > 0 || sendingCode ? 'text-gray-400 bg-gray-50' : 'text-indigo-600'"
              >
                <svg v-if="sendingCode" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ sendingCode ? '发送中...' : form.countdown > 0 ? `${form.countdown}s` : '获取验证码' }}
              </button>
            </div>
          </div>

          <!-- 密码输入 -->
          <div>
            <label for="password" class="block text-sm font-medium leading-6 text-gray-900">密码</label>
            <div class="mt-2 relative">
              <input 
                id="password" 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'" 
                required
                placeholder="请输入密码"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
              />
              <button 
                type="button" 
                @click="togglePassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <svg v-if="showPassword" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 服务条款 -->
          <div class="flex items-center">
            <input 
              id="agree-terms" 
              v-model="agreed" 
              type="checkbox" 
              required
              class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600" 
            />
            <label for="agree-terms" class="ml-3 block text-sm leading-6 text-gray-900">
              我已阅读并同意
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">服务条款</a>
              和
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">隐私政策</a>
            </label>
          </div>

          <!-- 注册按钮 -->
          <div>
            <button 
              type="submit" 
              :disabled="!isFormValid || loading"
              class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? '注册中...' : '注册' }}
            </button>
          </div>
        </form>

        <!-- 登录链接 -->
        <div>
          <div class="relative mt-10">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
              <div class="w-full border-t border-gray-200"></div>
            </div>
            <div class="relative flex justify-center text-sm font-medium leading-6">
              <span class="bg-white px-6 text-gray-900">已有账号?</span>
            </div>
          </div>

          <div class="mt-6">
            <router-link 
              to="/login"
              class="flex w-full justify-center rounded-md bg-white px-3 py-1.5 text-sm font-semibold leading-6 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              登录
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { showToast } from '@/components/ToastMessage'
import { register, sendSmsCode } from '@/api/user'
import { SMS_SCENE } from '@/store'
import HeadView from '@/components/HeadView.vue'

/**
 * Vuex store 实例
 * @type {import('vuex').Store}
 */
const store = useStore()

/**
 * Vue Router 实例
 * @type {import('vue-router').Router}
 */
const router = useRouter()

/**
 * 表单数据
 * @type {import('vue').Ref<Object>}
 */
const form = ref({
  phone: '',
  password: '',
  code: '',
  countdown: 0
})

/**
 * UI 状态变量
 */
const showPassword = ref(false)
const agreed = ref(false)
const loading = ref(false)
const sendingCode = ref(false)

/**
 * 表单验证计算属性
 * @type {import('vue').ComputedRef<boolean>}
 */
const isFormValid = computed(() => {
  return form.value.phone && 
         form.value.code && 
         form.value.password && 
         form.value.password.length >= 6 && 
         agreed.value
})

/**
 * 切换密码显示状态
 */
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

/**
 * 统一错误处理函数
 * @param {Error} error - 错误对象
 * @param {Object} options - 处理选项
 * @param {string} options.type - 错误类型 ('register'|'sendCode')
 * @param {Function} options.onRegistered - 已注册回调
 */
 const handleError = (error, { type, onRegistered }) => {
  const errorData = error.response?.data
  
  // 处理已注册错误
  if (errorData?.errors?.phone?.[0]?.includes('已注册')) {
    showToast('手机号已注册', 'warning')
    onRegistered()
    return
  }
  
  // 处理验证码错误
  if (errorData?.errors?.code?.[0]?.includes('验证码')) {
    showToast('验证码错误或已过期，请重新获取', 'error')
    return
  }
  
  // 处理其他业务错误
  if (errorData?.message) {
    showToast(errorData.message, 'error')
    return
  }
  
  // 处理默认错误
  const defaultMessages = {
    sendCode: '发送验证码失败，请稍后重试',
    register: '注册失败，请稍后重试'
  }
  showToast(defaultMessages[type], 'error')
}

/**
 * 获取验证码
 */
const getVerifyCode = async () => {
  if (!checkNetwork()) return
  
  if (!form.value.phone) {
    showToast('请输入手机号', 'warning')
    return
  }
  
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(form.value.phone)) {
    showToast('请输入正确的手机号', 'warning')
    return
  }

  try {
    sendingCode.value = true
    const response = await sendSmsCode({
      phone: form.value.phone,
      scene: SMS_SCENE.REGISTER
    })
    
    if (response.data.code === 200) {
      form.value.countdown = 60
      const timer = setInterval(() => {
        form.value.countdown--
        if (form.value.countdown <= 0) {
          clearInterval(timer)
        }
      }, 1000)
      
      showToast('验证码已发送', 'success')
    }
  } catch (error) {
    handleError(error, {
      type: 'sendCode',
      onRegistered: () => router.push('/login')
    })
  } finally {
    sendingCode.value = false
  }
}

/**
 * 注册处理
 */
const handleRegister = async () => {
  if (!checkNetwork()) return
  
  if (!isFormValid.value) {
    showToast('请填写完整信息并同意服务条款', 'warning')
    return
  }

  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(form.value.phone)) {
    showToast('请输入正确的手机号', 'warning')
    return
  }

  try {
    loading.value = true
    const registerResponse = await register({
      phone: form.value.phone,
      password: form.value.password,
      code: form.value.code
    })
    
    if (registerResponse.data.code === 200) {
      try {
        await store.dispatch('loginWithPassword', {
          credentials: {
            phone: form.value.phone,
            password: form.value.password
          },
          remember: true
        })
        
        showToast('注册成功', 'success')
        await new Promise(resolve => setTimeout(resolve, 100))
        router.push('/user')
      } catch (loginError) {
        showToast('注册成功，请手动登录', 'info')
        router.push('/login')
      }
    }
  } catch (error) {
    handleError(error, {
      type: 'register',
      onRegistered: () => router.push('/login')
    })
  } finally {
    loading.value = false
  }
}

/**
 * 检查网络连接状态
 * @returns {boolean} 网络是否可用
 */
const checkNetwork = () => {
  if (!navigator.onLine) {
    showToast('网络连接不稳定，请检查网络设置', 'warning')
    return false
  }
  return true
}

/**
 * 网络恢复处理
 */
const handleOnline = () => {
  showToast('网络已连接', 'success')
}

/**
 * 网络断开处理
 */
const handleOffline = () => {
  showToast('网络连接已断开', 'warning')
}

// 生命周期钩子
onMounted(() => {
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
})

onUnmounted(() => {
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
})
</script>