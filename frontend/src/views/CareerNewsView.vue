<template>
    <HeadView />
    <div class="bg-gray-100 min-h-screen pt-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">职场资讯</h1>
        
        <!-- 文章列表 -->
        <div class="space-y-6">
          <article v-for="i in 5" :key="i" class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="p-6">
              <div class="flex items-center gap-x-4 text-xs">
                <time class="text-gray-500">2024-01-{{ i }}</time>
                <a href="#" class="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">
                  职场经验
                </a>
              </div>
              <div class="group relative">
                <h3 class="mt-3 text-lg font-semibold leading-6 text-gray-900">
                  <a href="#">
                    <span class="absolute inset-0"></span>
                    职场进阶必备技能：如何提升你的职业竞争力
                  </a>
                </h3>
                <p class="mt-5 line-clamp-3 text-sm leading-6 text-gray-600">
                  在当今快速发展的职场环境中，持续学习和提升自己变得越来越重要。本文将为您详细介绍如何有效提升职业竞争力，包括技能培养、人际关系处理等多个方面。
                </p>
              </div>
              <div class="mt-6 flex border-t border-gray-900/5 pt-6">
                <div class="relative flex items-center gap-x-4">
                  <img src="https://via.placeholder.com/40" alt="" class="h-10 w-10 rounded-full bg-gray-50">
                  <div class="text-sm leading-6">
                    <p class="font-semibold text-gray-900">
                      <a href="#">
                        <span class="absolute inset-0"></span>
                        职场专家
                      </a>
                    </p>
                    <p class="text-gray-600">职业发展顾问</p>
                  </div>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
    <FootView />
  </template>
  
  <script>
  import HeadView from '@/components/HeadView.vue'
  import FootView from '@/components/FootView.vue'
  
  export default {
    name: 'CareerNewsView',
    components: {
      HeadView,
      FootView
    }
  }
  </script>