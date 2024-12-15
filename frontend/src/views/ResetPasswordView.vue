<template>
    <HeadView />
    <div class="bg-gray-100">
        <div class="flex min-h-full items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
            <div class="w-full max-w-sm space-y-10">
                <div>
                    <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">重置密码</h2>
                </div>

                <form class="space-y-6" @submit.prevent="handleResetPassword">
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
                                placeholder="请输入新密码"
                                v-model="form.new_password"
                            >
                        </div>
                        <div class="-mt-px">
                            <input type="password" required
                                class="block w-full rounded-b-md bg-white px-3 py-1.5 text-[14px] text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-0"
                                placeholder="请确认新密码"
                                v-model="form.confirm_password"
                            >
                        </div>
                    </div>

                    <button type="submit" 
                        class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-[14px] font-semibold leading-6 text-white hover:bg-indigo-500"
                        :disabled="loading"
                    >
                        {{ loading ? '提交中...' : '重置密码' }}
                    </button>

                    <p class="text-center text-sm text-gray-500">
                        <router-link to="/login" class="font-semibold text-indigo-600 hover:text-indigo-500">返回登录</router-link>
                    </p>
                </form>
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
    name: 'ResetPasswordView',
    components: {
        HeadView,
        FootView,
        ToastMessage
    },
    data() {
        return {
            form: {
                phone: '',
                code: '',
                new_password: '',
                confirm_password: ''
            },
            loading: false,
            countdown: 0,
            timer: null
        }
    },
    methods: {
        showToast(message) {
            this.$refs.toast.showMessage(message)
        },

        // 发送验证码
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
                    scene: 'reset_password'  // 重置密码场景
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

        // 重置密码
        async handleResetPassword() {
            if (!this.form.phone) {
                this.showToast('请输入手机号')
                return
            }
            if (!this.form.code) {
                this.showToast('请输入验证码')
                return
            }
            if (!this.form.new_password) {
                this.showToast('请输入新密码')
                return
            }
            if (!this.form.confirm_password) {
                this.showToast('请确认新密码')
                return
            }
            if (this.form.new_password !== this.form.confirm_password) {
                this.showToast('两次输入的密码不一致')
                return
            }

            this.loading = true
            try {
                const response = await axios.post('/api/users/reset-password/', {
                    phone: this.form.phone,
                    code: this.form.code,
                    new_password: this.form.new_password,
                    confirm_password: this.form.confirm_password
                })

                if (response.data.code === 200) {
                    this.showToast('密码重置成功')
                    // 延迟跳转到登录页
                    setTimeout(() => {
                        this.$router.push('/login')
                    }, 1500)
                }
            } catch (error) {
                if (error.response) {
                    const { data } = error.response
                    if (data.errors) {
                        const firstError = Object.values(data.errors)[0][0]
                        this.showToast(firstError)
                    } else {
                        this.showToast(data.message || '重置密码失败')
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