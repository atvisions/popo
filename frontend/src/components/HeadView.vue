<template>
    <header class="bg-white fixed top-0 left-0 right-0 z-50">
        <nav class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8">
            <!-- Logo -->
            <div class="flex">
                <a href="/" class="-m-1.5 p-1.5">
                    <span class="sr-only">popo.work</span>
                    <img class="h-8 w-auto" src="../assets/images/logo.png" alt="">
                </a>
            </div>

            <!-- 中间导航 -->
            <div class="flex gap-x-12">
                <router-link 
                    to="/" 
                    class="text-sm font-semibold leading-6"
                    :class="{'text-indigo-600': isCurrentRoute('/'), 'text-gray-900': !isCurrentRoute('/')}"
                >
                    首页
                </router-link>
                <router-link 
                    to="/templates" 
                    class="text-sm font-semibold leading-6"
                    :class="{'text-indigo-600': isCurrentRoute('/templates'), 'text-gray-900': !isCurrentRoute('/templates')}"
                >
                    简历模版
                </router-link>
                <router-link 
                    to="/news" 
                    class="text-sm font-semibold leading-6"
                    :class="{'text-indigo-600': isCurrentRoute('/news'), 'text-gray-900': !isCurrentRoute('/news')}"
                >
                    职场资讯
                </router-link>
                <router-link 
                    to="/faq" 
                    class="text-sm font-semibold leading-6"
                    :class="{'text-indigo-600': isCurrentRoute('/faq'), 'text-gray-900': !isCurrentRoute('/faq')}"
                >
                    常见问题
                </router-link>
                <router-link 
                    to="/pro" 
                    class="text-sm font-semibold leading-6"
                    :class="{'text-indigo-600': isCurrentRoute('/pro'), 'text-gray-900': !isCurrentRoute('/pro')}"
                >
                    PRO +
                </router-link>
            </div>

            <!-- 右侧登录/用户信息 -->
            <div class="flex items-center">
                <template v-if="!isLoggedIn">
                    <router-link to="/login" class="text-sm font-semibold leading-6 text-gray-900 mr-4">登录</router-link>
                    <router-link to="/register" class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">注册</router-link>
                </template>
                
                <template v-else>
                    <div class="relative">
                        <button type="button" @click.stop="toggleDropdown" class="flex items-center text-sm font-semibold leading-6 text-gray-900">
                            {{ userPhone }}
                            <svg class="ml-2 h-5 w-5" :class="{ 'transform rotate-180': showDropdown }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>
                        
                        <div v-show="showDropdown" class="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
                            <div class="py-1">
                                <router-link to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">个人主页</router-link>
                                <button @click="handleLogout" class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    退出登录
                                </button>
                            </div>
                        </div>
                    </div>
                </template>
            </div>
        </nav>
    </header>
</template>

<script>
export default {
    name: 'HeadView',
    data() {
        return {
            showDropdown: false,
            userPhone: ''
        }
    },
    computed: {
        isLoggedIn() {
            return !!localStorage.getItem('access_token')
        }
    },
    methods: {
        toggleDropdown() {
            this.showDropdown = !this.showDropdown
        },
        handleLogout() {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('user_phone')
            this.showDropdown = false
            window.location.href = '/'
        },
        formatPhone(phone) {
            if (!phone) return ''
            return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
        },
        initUserInfo() {
            const phone = localStorage.getItem('user_phone')
            if (phone) {
                this.userPhone = this.formatPhone(phone)
            }
        },
        handleClickOutside(e) {
            if (!this.$el.contains(e.target)) {
                this.showDropdown = false
            }
        },
        isCurrentRoute(path) {
            return this.$route.path === path
        }
    },
    mounted() {
        this.initUserInfo()
        document.addEventListener('click', this.handleClickOutside)
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside)
    }
}
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
    transition: all 0.3s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>