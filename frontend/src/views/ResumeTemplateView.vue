<template>
    <HeadView />
    <div class="bg-gray-100 min-h-screen pt-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">简历模板</h1>
        
        <!-- 模板列表 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- 示例模板卡片 -->
          <div v-for="i in 6" :key="i" class="bg-white rounded-lg shadow-md overflow-hidden">
            <img src="https://via.placeholder.com/400x300" alt="简历模板预览" class="w-full h-48 object-cover">
            <div class="p-4">
              <h3 class="text-lg font-semibold text-gray-900">简历模板 {{ i }}</h3>
              <p class="mt-2 text-sm text-gray-600">专业的简历模板，助您打造完美简历</p>
              <button class="mt-4 w-full bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-500">
                使用此模板
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <FootView />
  </template>
  
  <script>
  import HeadView from '@/components/HeadView.vue'
  import FootView from '@/components/FootView.vue'
  
  export default {
    name: 'ResumeTemplateView',
    components: {
      HeadView,
      FootView
    }
  }
  </script>