<template>
    <HeadView />
    <div class="bg-gray-100">
        <div class="flex min-h-full items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
            <div class="w-full max-w-sm space-y-10">
                <div>
                    <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">账号登录</h2>
                </div>

                <!-- 登录方式切换 -->
                <div class="flex justify-center space-x-8">
                    <button 
                        :class="{'text-indigo-600 border-b-2 border-indigo-600': loginType === 'account'}"
                        class="pb-2" 
                        @click="loginType = 'account'"
                    >
                        账号密码登录
                    </button>
                    <button 
                        :class="{'text-indigo-600 border-b-2 border-indigo-600': loginType === 'phone'}"
                        class="pb-2"
                        @click="loginType = 'phone'"
                    >
                        手机验证码登录
                    </button>
                </div>

                <!-- 账号密码登录表单 -->
                <form v-if="loginType === 'account'" class="space-y-6" @submit.prevent="handleLogin">
                    <div>
                        <input type="text" required
                            class="block w-full rounded-t-md bg-white px-3 py-1.5 text-sm text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0"
                            placeholder="请输入用户名/手机号"
                            v-model="accountForm.username"
                        >
                        <input type="password" required
                            class="block w-full rounded-b-md bg-white px-3 py-1.5 text-sm text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0 -mt-px"
                            placeholder="请输入密码"
                            v-model="accountForm.password"
                        >
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <input type="checkbox" v-model="accountForm.remember" class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600">
                            <label class="ml-2 block text-sm text-gray-900">记住我</label>
                        </div>
                        <router-link to="/reset-password" class="text-sm font-semibold text-indigo-600 hover:text-indigo-500">忘记密码?</router-link>
                    </div>

                    <button type="submit" 
                        class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white hover:bg-indigo-500"
                        :disabled="loading"
                    >
                        {{ loading ? '登录中...' : '登录' }}
                    </button>
                </form>

                <!-- 手机验证码登录表单 -->
                <form v-else class="space-y-6" @submit.prevent="handleLogin">
                    <div>
                        <input type="tel" required
                            class="block w-full rounded-t-md bg-white px-3 py-1.5 text-sm text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0"
                            placeholder="请输入手机号"
                            v-model="phoneForm.phone"
                        >
                        <div class="flex -mt-px">
                            <input type="text" required
                                class="block w-full bg-white px-3 py-1.5 text-sm text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0"
                                placeholder="请输入验证码"
                                v-model="phoneForm.code"
                            >
                            <button type="button" 
                                class="bg-indigo-600 px-8 text-sm text-white hover:bg-indigo-500 whitespace-nowrap disabled:bg-gray-400"
                                @click="sendCode"
                                :disabled="countdown > 0"
                            >
                                {{ countdown > 0 ? `${countdown}秒后重试` : '获取验证码' }}
                            </button>
                        </div>
                    </div>

                    <button type="submit" 
                        class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white hover:bg-indigo-500"
                        :disabled="loading"
                    >
                        {{ loading ? '登录中...' : '登录' }}
                    </button>
                </form>

                <p class="text-center text-sm text-gray-500">
                    还没有账号？
                    <router-link to="/register" class="font-semibold text-indigo-600 hover:text-indigo-500">立即注册</router-link>
                </p>
            </div>
        </div>
    </div>
    <FootView />
    <ToastMessage ref="toast"/>
</template>

<script>
import axios from 'axios'
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'
import ToastMessage from '@/components/ToastMessage.vue'

export default {
    name: 'LoginView',
    components: {
        HeadView,
        FootView,
        ToastMessage
    },
    data() {
        return {
            loginType: 'account', // account 或 phone
            loading: false,
            countdown: 0,
            timer: null,
            accountForm: {
                username: '',
                password: '',
                remember: false
            },
            phoneForm: {
                phone: '',
                code: ''
            }
        }
    },
    methods: {
        showToast(message) {
            this.$refs.toast.showMessage(message)
        },

        // 发送验证码
        async sendCode() {
            if (!this.phoneForm.phone) {
                this.showToast('请输入手机号')
                return
            }
            if (!/^1[3-9]\d{9}$/.test(this.phoneForm.phone)) {
                this.showToast('请输入正确的手机号')
                return
            }

            try {
                const response = await axios.post('/api/users/sms/code/', {
                    phone: this.phoneForm.phone,
                    scene: 'login',      // 修改为 login
                    login_mode: 'code'   // 添加 login_mode 参数
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

        // 登录处理
        async handleLogin() {
            if (this.loginType === 'account') {
                if (!this.accountForm.username) {
                    this.showToast('请输入手机号')
                    return
                }
                if (!this.accountForm.password) {
                    this.showToast('请输入密码')
                    return
                }
            } else {
                if (!this.phoneForm.phone) {
                    this.showToast('请输入手机号')
                    return
                }
                if (!this.phoneForm.code) {
                    this.showToast('请输入验证码')
                    return
                }
            }

            this.loading = true
            try {
                let response
                if (this.loginType === 'account') {
                    // 账号密码登录
                    response = await axios.post('/api/users/login/password/', {
                        phone: this.accountForm.username,
                        password: this.accountForm.password
                    })
                } else {
                    // 手机验证码登录 - 修改为正确的接口
                    response = await axios.post('/api/users/login/code/', {
                        phone: this.phoneForm.phone,
                        code: this.phoneForm.code
                    })
                }

                if (response.data.code === 200) {
                    this.showToast('登录成功')
                    // 保存token和用户信息
                    localStorage.setItem('access_token', response.data.data.tokens.access)
                    localStorage.setItem('refresh_token', response.data.data.tokens.refresh)
                    localStorage.setItem('user_phone', this.loginType === 'account' ? this.accountForm.username : this.phoneForm.phone)
                    
                    // 延迟跳转
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
                        this.showToast(data.message || '登录失败')
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