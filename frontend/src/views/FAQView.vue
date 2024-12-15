<template>
    <HeadView />
    <div class="bg-gray-100 min-h-screen pt-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">常见问题</h1>
        
        <!-- FAQ列表 -->
        <div class="space-y-4">
          <div v-for="i in 5" :key="i" class="bg-white rounded-lg shadow-md overflow-hidden">
            <button 
              @click="toggleFAQ(i)" 
              class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50"
            >
              <span class="text-lg font-medium text-gray-900">如何创建一份专业的简历？</span>
              <svg 
                class="h-5 w-5 text-gray-500 transform transition-transform duration-200"
                :class="{ 'rotate-180': openFAQ === i }"
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div v-show="openFAQ === i" class="px-6 py-4 border-t border-gray-200">
              <p class="text-gray-600">
                创建专业简历的关键步骤包括：
                1. 选择合适的模板
                2. 突出你的核心技能和经验
                3. 使用具体的数据和成就来支持你的能力
                4. 确保简历格式统一和专业
                5. 根据不同的职位需求适当调整内容
              </p>
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
    name: 'FAQView',
    components: {
      HeadView,
      FootView
    },
    data() {
      return {
        openFAQ: null
      }
    },
    methods: {
      toggleFAQ(index) {
        this.openFAQ = this.openFAQ === index ? null : index
      }
    }
  }
  </script>