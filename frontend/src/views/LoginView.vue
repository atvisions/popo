<template>
  <HeadView />
  <div class="min-h-screen bg-gray-50 pt-14">
    <!-- Logo 部分 -->
    <div class="sm:mx-auto sm:w-full sm:max-w-md pt-8">
      <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">登录账号</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
      <div class="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <!-- 手机号输入 -->
          <div>
            <label for="phone" class="block text-sm font-medium leading-6 text-gray-900">手机号</label>
            <div class="mt-2">
              <input 
                type="tel" 
                id="phone" 
                v-model="phone"
                required
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                :class="{'ring-red-300': phoneError}"
              >
              <div v-if="phoneError" class="mt-1 text-sm text-red-600">{{ phoneError }}</div>
            </div>
          </div>

          <!-- 密码输入 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">密码</label>
            <div class="mt-2 relative">
              <input 
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="password"
                required
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3 pr-10"
                :class="{'ring-red-300': passwordError}"
              >
              <button 
                type="button"
                @click="togglePassword"
                class="absolute inset-y-0 right-0 flex items-center pr-3"
              >
                <svg v-if="showPassword" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
            <div v-if="passwordError" class="mt-1 text-sm text-red-600">{{ passwordError }}</div>
          </div>

          <!-- 记住我和忘记密码 -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input 
                id="remember-me" 
                type="checkbox"
                v-model="rememberMe"
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-600 border-gray-300 rounded"
              >
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">记住我</label>
            </div>

            <div class="text-sm">
              <router-link to="/reset-password" class="font-medium text-indigo-600 hover:text-indigo-500">
                忘记密码？
              </router-link>
            </div>
          </div>

          <!-- 登录按钮 -->
          <div>
            <button 
              type="submit"
              :disabled="!isFormValid"
              class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </div>
        </form>

        <!-- 其他登录方式 -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="bg-white px-2 text-gray-500">其他登录方式</span>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-3 gap-3">
            <div>
              <a href="#" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                <span class="sr-only">微信登录</span>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.81-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.595-6.348z"/>
                </svg>
              </a>
            </div>

            <div>
              <a href="#" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                <span class="sr-only">QQ登录</span>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.003 2c-2.265 0-6.29 1.364-6.29 7.325v1.195S3.55 14.96 3.55 17.474c0 .665.17 1.025.281 1.025.114 0 .902-.484 1.748-2.072 0 0-.18 2.197 1.904 3.967 0 0-1.77.495-1.77 1.182 0 .686 4.078.43 6.29.43 2.213 0 6.29.256 6.29-.43 0-.687-1.77-1.182-1.77-1.182s2.085-1.77 1.905-3.967c.846 1.588 1.634 2.072 1.746 2.072.111 0 .283-.36.283-1.025 0-2.514-2.166-6.954-2.166-6.954V9.325C18.29 3.364 14.268 2 12.003 2z"/>
                </svg>
              </a>
            </div>

            <div>
              <a href="#" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                <span class="sr-only">微博登录</span>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M10.098 20.323c-3.977.391-7.414-1.406-7.672-4.02-.259-2.609 2.759-5.047 6.74-5.441 3.979-.394 7.413 1.404 7.672 4.018.259 2.6-2.759 5.049-6.74 5.443z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import HeadView from '@/components/HeadView.vue'
import { showToast } from '@/components/ToastMessage'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const phone = ref('')
const password = ref('')
const loading = ref(false)
const rememberMe = ref(false)
const showPassword = ref(false)

// 表单验证状态
const isFormValid = computed(() => {
    return phone.value && password.value && !loading.value
})

// 手机号验证
const validatePhone = () => {
    const phoneRegex = /^1[3-9]\d{9}$/
    if (!phone.value) {
        showToast('请输入手机号', 'warning')
        return false
    }
    if (!phoneRegex.test(phone.value)) {
        showToast('请输入正确的手机号', 'warning')
        return false
    }
    return true
}

// 密码验证
const validatePassword = () => {
    if (!password.value) {
        showToast('请输入密码', 'warning')
        return false
    }
    if (password.value.length < 6) {
        showToast('密码长度不能少于6位', 'warning')
        return false
    }
    return true
}

// 登录处理
const handleLogin = async () => {
    if (!validatePhone() || !validatePassword()) return

    try {
        loading.value = true
        const response = await axios.post('/api/users/login/password/', {
            phone: phone.value,
            password: password.value
        })

        if (response.data.code === 200) {
            // 从响应中获取数据
            const { tokens, user } = response.data.data
            
            // 保存登录信息
            localStorage.setItem('access_token', tokens.access)
            localStorage.setItem('refresh_token', tokens.refresh)
            localStorage.setItem('user_phone', user.phone)
            localStorage.setItem('user_id', user.id)

            // 提示并跳转
            showToast(response.data.message || '登录成功！', 'success')
            router.push('/')
        }
    } catch (error) {
        console.error('登录错误:', error)
        if (error.response?.data) {
            const errorData = error.response.data
            const errorMessage = errorData.message || '登录失败，请重试'
            showToast(errorMessage, 'error')
        } else {
            showToast('登录失败，请重试', 'error')
        }
    } finally {
        loading.value = false
    }
}

// 切换密码显示
const togglePassword = () => {
    showPassword.value = !showPassword.value
}
</script>