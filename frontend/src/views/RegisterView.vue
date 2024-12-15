<template>
  <HeadView />
  <div class="bg-gray-100">
      <div class="flex min-h-full items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
          <div class="w-full max-w-sm space-y-10">
              <div>
                  <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">注册账号</h2>
              </div>

              <form class="space-y-6" @submit.prevent="handleRegister">
                  <div>
                      <div class="col-span-2">
                          <input type="tel" required
                              class="block w-full rounded-t-md bg-white px-3 py-1.5 text-sm text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0"
                              placeholder="请输入手机号"
                              v-model="form.phone"
                          >
                      </div>
                      <div class="-mt-px flex">
                          <input type="text" required
                              class="block w-full bg-white px-3 py-1.5 text-sm text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0"
                              placeholder="请输入验证码"
                              v-model="form.code"
                          >
                          <button type="button" 
                              class="bg-indigo-600 px-8 text-sm text-white hover:bg-indigo-500 whitespace-nowrap disabled:bg-gray-400"
                              @click="sendCode"
                              :disabled="countdown > 0"
                          >
                              {{ countdown > 0 ? `${countdown}秒后重试` : '获取验证码' }}
                          </button>
                      </div>
                      <div class="-mt-px">
                          <input type="password" required
                              class="block w-full bg-white px-3 py-1.5 text-[14px] text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0"
                              placeholder="请设置密码"
                              v-model="form.password"
                          >
                      </div>
                      <div class="-mt-px">
                          <input type="password" required
                              class="block w-full rounded-b-md bg-white px-3 py-1.5 text-[14px] text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0"
                              placeholder="请确认密码"
                              v-model="form.confirm_password"
                          >
                      </div>
                  </div>

                  <div class="flex items-center">
                      <input id="terms" v-model="form.agreeTerms" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600">
                      <label for="terms" class="ml-3 block text-sm leading-6 text-gray-900">
                          我已阅读并同意
                          <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">用户协议</a>
                          和
                          <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">隐私政策</a>
                      </label>
                  </div>

                  <button type="submit" 
                      class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-[14px] font-semibold leading-6 text-white hover:bg-indigo-500"
                  >
                      注册
                  </button>
              </form>

              <p class="text-center text-sm text-gray-500">
                  已有账号？
                  <router-link to="/login" class="font-semibold text-indigo-600 hover:text-indigo-500">立即登录</router-link>
              </p>
          </div>
      </div>
  </div>
  <FootView />
  <ToastMessage ref="toast"/>
</template>

<script>
import axios from 'axios'
import ToastMessage from '@/components/ToastMessage.vue'
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'

export default {
    name: 'RegisterView',
    components: {
        ToastMessage,
        HeadView,
        FootView
    },
    data() {
        return {
            form: {
                phone: '',
                code: '',
                password: '',
                confirm_password: '',
                agreeTerms: false
            },
            errors: {},
            loading: false,
            countdown: 0,
            timer: null
        }
    },
    methods: {
        // 显示提示信息
        showToast(message) {
            this.$refs.toast.showMessage(message)
        },
        
        // 获取验证码
        async sendCode() {
            if (!this.form.phone) {
                this.showToast('请输入手机号')
                return
            }
            if (!/^1[3-9]\d{9}$/.test(this.form.phone)) {
                this.showToast('请输入正确的手机号')
                return
            }

            try {
                const response = await axios.post('/api/users/sms/code/', {
                    phone: this.form.phone,
                    scene: 'register'
                })

                if (response.data.code === 200) {
                    this.showToast('验证码已发送')
                    this.countdown = 60
                    this.timer = setInterval(() => {
                        if (this.countdown > 0) {
                            this.countdown--
                        } else {
                            clearInterval(this.timer)
                        }
                    }, 1000)
                }
            } catch (error) {
                if (error.response) {
                    const { data } = error.response
                    if (data.errors) {
                        const firstError = Object.values(data.errors)[0][0]
                        this.showToast(firstError)
                    } else {
                        this.showToast(data.message || '发送验证码失败')
                    }
                } else {
                    this.showToast('网络错误，请稍后重试')
                }
            }
        },

        // 注册处理
        async handleRegister() {
            if (!this.form.phone) {
                this.showToast('请输入手机号')
                return
            }
            if (!this.form.code) {
                this.showToast('请输入验证码')
                return
            }
            if (!this.form.password) {
                this.showToast('请设置密码')
                return
            }
            if (!this.form.confirm_password) {
                this.showToast('请确认密码')
                return
            }
            if (this.form.password !== this.form.confirm_password) {
                this.showToast('两次输入的密码不一致')
                return
            }
            if (!this.form.agreeTerms) {
                this.showToast('请阅读并同意用户协议和隐私政策')
                return
            }

            this.loading = true
            try {
                const response = await axios.post('/api/users/register/', {
                    phone: this.form.phone,
                    code: this.form.code,
                    password: this.form.password,
                    confirm_password: this.form.confirm_password
                })

                if (response.data.code === 200) {
                  this.showToast('注册成功')
                  // 保存token和手机号
                  localStorage.setItem('access_token', response.data.data.tokens.access)
                  localStorage.setItem('refresh_token', response.data.data.tokens.refresh)
                  localStorage.setItem('user_phone', this.form.phone)  // 添加这行
                  
                  // 延迟跳转，让用户看到成功提示
                  setTimeout(() => {
                      this.$router.push('/')
                  }, 1500)
              }
            } catch (error) {
                if (error.response) {
                    const { data } = error.response
                    if (data.errors) {
                        const firstError = Object.values(data.errors)[0][0]
                        this.showToast(firstError)
                    } else {
                        this.showToast(data.message || '注册失败')
                    }
                } else {
                    this.showToast('网络错误，请稍后重试')
                }
            } finally {
                this.loading = false
            }
        }
    },
    beforeUnmount() {
        if (this.timer) {
            clearInterval(this.timer)
        }
    }
}
</script>