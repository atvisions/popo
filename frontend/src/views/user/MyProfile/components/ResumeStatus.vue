<!-- src/views/user/MyProfile/components/ResumeStatus.vue -->
<template>
    <div class="bg-white rounded-lg shadow">
      <div class="p-4">
        <!-- 标题和百分比 -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-base font-medium text-gray-900">简历完整度</h3>
          <span class="text-lg font-semibold" :class="progressTextColorClass">
            {{ completionRate }}%
          </span>
        </div>
  
        <!-- 进度条 -->
        <div class="bg-gray-200 rounded-full h-2.5 mb-3">
          <div 
            class="h-2.5 rounded-full transition-all duration-500"
            :class="progressColorClass"
            :style="{ width: `${completionRate}%` }"
          ></div>
        </div>
  
        <!-- 提示信息 -->
        <p class="text-sm mb-4" :class="progressTextColorClass">
          {{ progressMessage }}
        </p>
  
        <!-- 操作按钮 -->
        <div class="grid grid-cols-3 gap-3">
          <button
            @click="$emit('ai-optimize')"
            class="flex items-center justify-center px-4 py-2 rounded-lg text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-sm"
          >
            <SparklesIcon class="w-4 h-4 mr-1.5" />
            AI优化
          </button>
  
          <button
            @click="$emit('import')"
            class="flex items-center justify-center px-4 py-2 rounded-lg text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 transition-all duration-200"
          >
            <ArrowDownTrayIcon class="w-4 h-4 mr-1.5" />
            导入简历
          </button>
  
          <button
            @click="$emit('preview')"
            class="flex items-center justify-center px-4 py-2 rounded-lg text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 transition-all duration-200"
          >
            <EyeIcon class="w-4 h-4 mr-1.5" />
            预览简历
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { 
    SparklesIcon,
    ArrowDownTrayIcon,
    EyeIcon 
  } from '@heroicons/vue/24/outline'
  
  const props = defineProps({
    completionRate: {
      type: Number,
      default: 0
    },
    loading: {
      type: Boolean,
      default: false
    }
  })
  
  defineEmits(['ai-optimize', 'import', 'preview'])
  
  const progressColorClass = computed(() => {
    if (props.completionRate >= 80) return 'bg-green-500'
    if (props.completionRate >= 50) return 'bg-yellow-500'
    return 'bg-red-500'
  })
  
  const progressTextColorClass = computed(() => {
    if (props.completionRate >= 80) return 'text-green-600'
    if (props.completionRate >= 50) return 'text-yellow-600'
    return 'text-red-600'
  })
  
  const progressMessage = computed(() => {
    if (props.completionRate >= 80) return '您的简历完整度很高，继续保持！'
    if (props.completionRate >= 50) return '简历完整度一般，建议继续完善。'
    return '简历完整度较低，请尽快完善简历信息。'
  })
  </script>

<style scoped>
/* 添加按钮悬停效果 */
button {
  position: relative;
  overflow: hidden;
}

button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translate(-50%, -50%) scale(0);
  border-radius: inherit;
  transition: transform 0.3s ease;
}

button:hover::after {
  transform: translate(-50%, -50%) scale(1.5);
}

/* 渐变进度条效果 */
.bg-green-500 {
  background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
}

.bg-yellow-500 {
  background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 100%);
}

.bg-red-500 {
  background: linear-gradient(90deg, #EF4444 0%, #F87171 100%);
}
</style>