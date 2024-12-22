<template>
    <div class="space-y-6">
      <!-- 账户安全 -->
      <section class="bg-white rounded-lg p-6 shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-6">账户安全</h2>
        
        <!-- 手机号 -->
        <div class="space-y-6">
          <div class="flex items-center justify-between py-4 border-b">
            <div>
              <h3 class="text-base font-medium text-gray-900">手机号</h3>
              <p class="mt-1 text-sm text-gray-500">{{ maskPhone(userPhone) }}</p>
            </div>
            <button @click="showPhoneModal = true"
              class="px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors">
              更换手机号
            </button>
          </div>
  
          <!-- 微信绑定 -->
            <div class="flex items-center justify-between py-4 border-b">
            <div>
                <h3 class="text-base font-medium text-gray-900">微信绑定</h3>
                <p class="mt-1 text-sm text-gray-500">
                {{ userInfo.wechat ? `已绑定微信号：${maskWechat(userInfo.wechat)}` : '未绑定' }}
                </p>
            </div>
            <button 
                @click="handleWechatBinding"
                class="px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors"
            >
                {{ userInfo.wechat ? '更换绑定' : '立即绑定' }}
            </button>
            </div>
            <!-- 添加微信登录弹窗 -->
            <WeChatLoginModal
            :visible="showWeChatBindModal"
            :bind-mode="true"
            @close="showWeChatBindModal = false"
            @bind-success="handleWeChatBindSuccess"
            />

  
          <!-- 登录密码 -->
          <div class="flex items-center justify-between py-4 border-b">
            <div>
              <h3 class="text-base font-medium text-gray-900">登录密码</h3>
              <p class="mt-1 text-sm text-gray-500">定期更换密码可以帮助保护账号安全</p>
            </div>
            <button @click="showPasswordModal = true"
              class="px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors">
              修改密码
            </button>
          </div>
        </div>
      </section>
  
      <!-- 账号注销 -->
      <section class="bg-white rounded-lg p-6 shadow">
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0">
            <svg class="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div class="flex-grow">
            <h3 class="text-base font-medium text-gray-900">注销账号</h3>
            <p class="mt-1 text-sm text-gray-500">
              注销后，您的所有数据将被永久删除且无法恢复。请谨慎操作。
            </p>
            <button @click="showDeleteConfirm = true"
              class="mt-4 px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 transition-colors border border-red-600 rounded-md">
              注销账号
            </button>
          </div>
        </div>
      </section>
          <!-- 更换手机号弹窗 -->
    <div v-if="showPhoneModal"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">更换手机号</h3>
          <!-- 添加当前手机号显示 -->
      <div class="mb-6 p-4 bg-gray-50 rounded-md">
        <p class="text-sm text-gray-500">当前手机号：{{ maskPhone(userPhone) }}</p>
      </div>
          <form @submit.prevent="handlePhoneChange" class="space-y-4">
            <div>
              <label for="newPhone" class="block text-sm font-medium text-gray-700">新手机号</label>
              <input type="tel" id="newPhone" v-model="phoneForm.newPhone"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
            </div>
            <div>
              <label for="verifyCode" class="block text-sm font-medium text-gray-700">验证码</label>
              <div class="mt-1 flex rounded-md shadow-sm">
                <input type="text" id="verifyCode" v-model="phoneForm.verifyCode"
                  class="block w-full rounded-l-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
                  <button type="button" @click="sendPhoneCode"
                    class="relative inline-flex items-center whitespace-nowrap rounded-r-md border border-gray-300 bg-gray-50 px-6 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500">
                    {{ phoneForm.countdown > 0 ? `${phoneForm.countdown}s` : '获取验证码' }}
                </button>
              </div>
            </div>
          </form>
        </div>
        <div class="bg-gray-50 px-6 py-4 flex justify-end space-x-3 rounded-b-lg">
          <button @click="showPhoneModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors">
            取消
          </button>
          <button @click="handlePhoneChange"
            class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-md transition-colors">
            确认更换
          </button>
        </div>
      </div>
    </div>

    <!-- 修改密码弹窗 -->
    <div v-if="showPasswordModal"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">修改密码</h3>
          <form @submit.prevent="handlePasswordChange" class="space-y-4">
            <!-- 当前密码 -->
            <div>
              <label for="old_password" class="block text-sm font-medium text-gray-700">当前密码</label>
              <div class="mt-1 relative">
                <input :type="showold_password ? 'text' : 'password'" 
                  id="old_password" 
                  v-model="passwordForm.old_password"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" 
                />
                <button type="button" 
                  @click="showold_password = !showold_password"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <svg v-if="showold_password" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- 新密码 -->
            <div>
              <label for="newPassword" class="block text-sm font-medium text-gray-700">新密码</label>
              <div class="mt-1 relative">
                <input :type="showNewPassword ? 'text' : 'password'" 
                  id="newPassword" 
                  v-model="passwordForm.newPassword"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" 
                />
                <button type="button" 
                  @click="showNewPassword = !showNewPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <svg v-if="showNewPassword" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- 确认新密码 -->
            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700">确认新密码</label>
              <div class="mt-1 relative">
                <input :type="showConfirmPassword ? 'text' : 'password'" 
                  id="confirmPassword" 
                  v-model="passwordForm.confirmPassword"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" 
                />
                <button type="button" 
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <svg v-if="showConfirmPassword" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                </button>
              </div>
            </div>
          </form>
        </div>
        <div class="bg-gray-50 px-6 py-4 flex justify-end space-x-3 rounded-b-lg">
          <button @click="closePasswordDialog"
            class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors">
            取消
          </button>
          <button @click="handlePasswordChange"
            class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="passwordLoading">
            <svg v-if="passwordLoading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            {{ passwordLoading ? '修改中...' : '确认修改' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 注销确认弹窗 -->
    <div v-if="showDeleteConfirm"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <div class="flex items-start space-x-3 mb-4">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-medium text-gray-900">确认注销账号？</h3>
              <p class="mt-2 text-sm text-gray-500">
                此操作将永久删除您的账号和所有相关数据，且无法恢复。请输入您的密码以确认。
              </p>
            </div>
          </div>

          <div class="mt-4">
            <label for="deletePassword" class="block text-sm font-medium text-gray-700">
              请输入密码确认
            </label>
            <div class="mt-1">
              <input type="password" id="deletePassword" v-model="deleteConfirmPassword"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm"
                placeholder="请输入您的登录密码" />
            </div>
          </div>
        </div>

        <div class="bg-gray-50 px-6 py-4 flex justify-end space-x-3 rounded-b-lg">
          <button @click="closeDeleteDialog"
            class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors">
            取消
          </button>
          <button @click="handleDeleteAccount"
            class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!deleteConfirmPassword || deleteLoading">
            <svg v-if="deleteLoading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            {{ deleteLoading ? '注销中...' : '确认注销' }}
          </button>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { showToast } from '@/components/ToastMessage'
import { changePhone, changePassword,sendSmsCode ,deleteAccount} from '@/api/user'  
const showWeChatBindModal = ref(false)


const store = useStore()
const router = useRouter()

// 用户信息 - 使用 computed
const userInfo = computed(() => store.getters.getUserInfo || {})
// 从 store 中获取用户手机号
const userPhone = computed(() => store.getters.getUserPhone)

// 模态框显示状态
const showPhoneModal = ref(false)
const showPasswordModal = ref(false)
const showDeleteConfirm = ref(false)
// 修改密码相关状态
const passwordLoading = ref(false)
// 注销相关状态
const deleteConfirmPassword = ref('')
const deleteLoading = ref(false)
// 手机号相关状态
const showold_password = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// 表单数据
const phoneForm = ref({
  newPhone: '',
  verifyCode: '',
  countdown: 0
})


const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 工具函数：信息脱敏
const maskPhone = (userPhone) => {
  if (!userPhone) return ''
  return userPhone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}


const maskWechat = (wechat) => {
  if (!wechat) return ''
  return wechat.substring(0, 3) + '***' + wechat.substring(wechat.length - 3)
}


// 关闭密码修改对话框
const closePasswordDialog = () => {
  showPasswordModal.value = false
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}
// 注销账户
const handleDeleteAccount = async () => {
  if (!deleteConfirmPassword.value) {
    showToast('请输入密码以确认注销', 'warning')
    return
  }

  try {
    deleteLoading.value = true
    await deleteAccount({
      password: deleteConfirmPassword.value
    })
    
    showToast('账号已注销成功', 'success')
    
    // 清除登录状态并跳转
    await store.dispatch('logout')
    router.push({
      path: '/login',
      query: { source: 'account_deleted' }  // 添加来源标记
    })
  } catch (error) {
    console.error('注销账号失败:', error)
    showToast(error.response?.data?.message || '注销账号失败，请检查密码是否正确', 'error')
  } finally {
    deleteLoading.value = false
    showDeleteConfirm.value = false
    deleteConfirmPassword.value = ''
  }
}

// 关闭注销对话框
const closeDeleteDialog = () => {
  showDeleteConfirm.value = false
  deleteConfirmPassword.value = ''
}
// 发送手机验证码
const sendPhoneCode = async () => {
  if (!phoneForm.value.newPhone) {
    showToast('请输入新手机号', 'warning')
    return
  }

  // 手机号格式验证
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(phoneForm.value.newPhone)) {
    showToast('请输入正确的手机号格式', 'warning')
    return
  }

  try {
    await sendSmsCode({  // 直接使用 API 函数
      phone: phoneForm.value.newPhone,
      scene: 'change_phone'  // 使用正确的场景值
    })
    
    // 开始倒计时
    phoneForm.value.countdown = 60
    const timer = setInterval(() => {
      phoneForm.value.countdown--
      if (phoneForm.value.countdown <= 0) {
        clearInterval(timer)
      }
    }, 1000)

    showToast('验证码已发送', 'success')
  } catch (error) {
    showToast(error.response?.data?.message || '发送验证码失败', 'error')
  }
}
// 更换手机号
const handlePhoneChange = async () => {
  if (!phoneForm.value.newPhone) {
    showToast('请输入新手机号', 'warning')
    return
  }

  // 手机号格式验证
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(phoneForm.value.newPhone)) {
    showToast('请输入正确的手机号格式', 'warning')
    return
  }

  if (!phoneForm.value.verifyCode) {
    showToast('请输入验证码', 'warning')
    return
  }

  try {
    await changePhone({
      phone: phoneForm.value.newPhone,
      code: phoneForm.value.verifyCode
    })
    
    showToast('手机号更换成功，请重新登录', 'success')
    showPhoneModal.value = false
    // 清空表单
    phoneForm.value = {
      newPhone: '',
      verifyCode: '',
      countdown: 0
    }

    // 登出并跳转到登录页
    await store.dispatch('logout')
    router.push({
      path: '/login',
      query: { redirect: router.currentRoute.value.fullPath }  // 保存当前页面路径
    })
  } catch (error) {
    console.error('更换手机号失败:', error)
    showToast(error.response?.data?.message || '更换手机号失败', 'error')
  }
}

// 修改密码
const handlePasswordChange = async () => {
  try {
    // 表单验证
    if (!passwordForm.value.old_password) {
      showToast('请输入当前密码', 'warning')
      return
    }
    if (!passwordForm.value.newPassword) {
      showToast('请输入新密码', 'warning')
      return
    }
    if (!passwordForm.value.confirmPassword) {
      showToast('请确认新密码', 'warning')
      return
    }
    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
      showToast('两次输入的新密码不一致', 'warning')
      return
    }
    if (passwordForm.value.newPassword.length < 6) {
      showToast('新密码长度不能少于6位', 'warning')
      return
    }
    if (passwordForm.value.old_password === passwordForm.value.newPassword) {
      showToast('新密码不能与当前密码相同', 'warning')
      return
    }

    passwordLoading.value = true
    await changePassword({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.newPassword,
      confirm_password: passwordForm.value.confirmPassword
    })

    showToast('密码修改成功，请重新登录', 'success')
    showPasswordModal.value = false
    
    // 清空表单
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    
    // 登出并跳转
    await store.dispatch('logout')
    router.push('/login')
  } catch (error) {
    console.error('修改密码失败:', error)
    const errorMessage = error.response?.data?.message 
      || error.response?.data?.errors?.old_password?.[0]
      || error.response?.data?.errors?.new_password?.[0]
      || error.message 
      || '修改密码失败，请检查当前密码是否正确'
    showToast(errorMessage, 'error')
  } finally {
    passwordLoading.value = false
  }
}
</script>