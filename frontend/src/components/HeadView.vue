<template>
    <header class="fixed w-full top-0 z-50 bg-white shadow">
        <nav class="mx-auto flex max-w-7xl items-center justify-between p-4 lg:px-8" aria-label="Global">
            <!-- Logo 区域 -->
            <div class="flex items-center space-x-4">
                <router-link to="/" class="flex items-center space-x-2">
                    <img src="../assets/images/logo.png" alt="" class="w-8 h-8">
                    <span class="hidden lg:block text-gray-500 text-xl">泡泡智造</span>
                </router-link>
            </div>

            <!-- 桌面端导航菜单 -->
            <div class="hidden lg:flex lg:gap-x-12">
                <router-link 
                    v-for="item in navigation" 
                    :key="item.name" 
                    :to="item.href"
                    :class="[
                        'text-sm font-semibold leading-6',
                        isCurrentRoute(item.href) 
                            ? 'text-indigo-600' 
                            : 'text-gray-900 hover:text-indigo-600'
                    ]"
                >
                    {{ item.name }}
                </router-link>
            </div>

            <!-- 桌面端登录注册按钮或用户菜单 -->
            <div class="hidden lg:flex items-center space-x-4">
                <template v-if="!isLoggedIn">
                    <router-link to="/login" 
                        class="text-sm font-semibold leading-6 text-gray-900 hover:text-indigo-600">
                        登录
                    </router-link>
                    <router-link to="/register" 
                        class="text-sm font-semibold leading-6 text-white bg-indigo-600 px-3 py-2 rounded-md hover:bg-indigo-500">
                        注册
                    </router-link>
                </template>
                <div v-else class="relative user-menu">
                    <button 
                        @click.stop="userMenuOpen = !userMenuOpen"
                        class="flex items-center space-x-2 text-sm font-semibold text-gray-900 hover:text-indigo-600"
                    >
                        <span>{{ userPhone }}</span>
                        <svg class="h-5 w-5" :class="{ 'rotate-180': userMenuOpen }" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                    </button>
                    
                    <!-- 用户下拉菜单 -->
                    <div v-if="userMenuOpen" 
                        class="absolute right-0 mt-2 w-48 rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5"
                        @click.stop
                    >
                        <router-link to="/user/center"
                            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                            @click="userMenuOpen = false">
                            用户中心
                        </router-link>
                        <button
                            @click="handleLogout"
                            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                            退出登录
                        </button>
                    </div>
                </div>
            </div>

            <!-- 移动端菜单按钮 -->
            <div class="lg:hidden">
                <button type="button" @click="toggleMenu" 
                    class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700">
                    <span class="sr-only">打开菜单</span>
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" 
                            d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                    </svg>
                </button>
            </div>
        </nav>

        <!-- 移动端菜单抽屉 -->
        <div v-if="mobileMenuOpen" 
            class="fixed inset-0 z-50"
            @click="toggleMenu">
            <div class="fixed inset-0 bg-black/25"></div>
            
            <div class="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10"
                @click.stop>
                <!-- 移动端菜单头部 -->
                <div class="flex items-center justify-between">
                    <router-link to="/" class="-m-1.5 p-1.5" @click="toggleMenu">
                        <div class="flex items-center space-x-2">
                            <img src="../assets/images/logo.png" alt="" class="w-8 h-8">
                            <span class="text-gray-500 text-xl">泡泡智造</span>
                        </div>
                    </router-link>
                    <button type="button" @click="toggleMenu" 
                        class="-m-2.5 rounded-md p-2.5 text-gray-700">
                        <span class="sr-only">关闭菜单</span>
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <!-- 移动端菜单内容 -->
                <div class="mt-6 flow-root">
                    <div class="-my-6 divide-y divide-gray-500/10">
                        <div class="space-y-2 py-6">
                            <router-link 
                                v-for="item in navigation" 
                                :key="item.name" 
                                :to="item.href"
                                :class="[
                                    '-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7',
                                    isCurrentRoute(item.href)
                                        ? 'text-indigo-600 bg-gray-50'
                                        : 'text-gray-900 hover:bg-gray-50'
                                ]"
                                @click="toggleMenu"
                            >
                                {{ item.name }}
                            </router-link>
                        </div>
                        <div class="py-6 space-y-2">
                            <template v-if="!isLoggedIn">
                                <router-link to="/login"
                                    class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                                    @click="toggleMenu">
                                    登录
                                </router-link>
                                <router-link to="/register"
                                    class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-white bg-indigo-600 hover:bg-indigo-500"
                                    @click="toggleMenu">
                                    注册
                                </router-link>
                            </template>
                            <template v-else>
                                <div class="-mx-3 px-3 py-2 text-base font-semibold leading-7 text-gray-900">
                                    {{ userPhone }}
                                </div>
                                <router-link to="/user/center"
                                    class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                                    @click="toggleMenu">
                                    用户中心
                                </router-link>
                                <button
                                    @click="handleLogout"
                                    class="-mx-3 block w-full text-left rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                                    退出登录
                                </button>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { showToast } from '@/components/ToastMessage'
import store from '@/store'

const router = useRouter()
const route = useRoute()
const mobileMenuOpen = ref(false)
const userMenuOpen = ref(false)

const navigation = [
    { name: '简历模板', href: '/templates' },
    { name: '职场资讯', href: '/news' },
    { name: '常见问题', href: '/faq' },
    { name: 'PRO +', href: '/pro' }
]

// 判断当前路由是否匹配
const isCurrentRoute = (href) => {
    return route.path === href
}

// 获取用户信息
const userPhone = computed(() => {
    return localStorage.getItem('user_phone')
})

const isLoggedIn = computed(() => {
    return !!userPhone.value
})

const toggleMenu = () => {
    mobileMenuOpen.value = !mobileMenuOpen.value
}

// 更新退出登录处理
const handleLogout = async () => {
    try {
        // 获取 refresh token
        const refreshToken = localStorage.getItem('refresh_token')
        
        // 调用退出接口
        await axios.post('/api/token/blacklist/', 
            { refresh: refreshToken }
        )
    } catch (error) {
        console.error('退出失败:', error)
    } finally {
        // 无论接口成功与否，都执行以下操作
        // 清除本地存储
        localStorage.clear()
        
        // 更新 store 状态
        store.commit('setLoginStatus', false)
        store.commit('setToken', null)
        
        // 关闭用户菜单
        userMenuOpen.value = false
        
        // 提示成功
        showToast('已退出登录', 'success')
        
        // 确保在状态更新后再跳转
        await router.push('/')
        
        // 强制刷新页面以确保状态完全更新
        window.location.reload()
    }
}

// 修改点击处理函数
const closeUserMenu = (e) => {
    // 如果点击的不是用户菜单区域，则关闭菜单
    if (!e.target.closest('.user-menu')) {
        userMenuOpen.value = false
    }
}

// 在组件挂载时添加点击事件监听
onMounted(() => {
    document.addEventListener('click', closeUserMenu)
})

// 在组件卸载时移除点击事件监听
onUnmounted(() => {
    document.removeEventListener('click', closeUserMenu)
})
</script>