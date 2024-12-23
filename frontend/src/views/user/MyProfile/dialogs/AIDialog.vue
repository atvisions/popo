<!-- src/views/user/MyProfile/dialogs/AIDialog.vue -->
<template>
    <el-dialog
      v-model="visible"
      title="AI 优化建议"
      width="640px"
    >
      <div v-loading="loading" class="min-h-[200px]">
        <template v-if="suggestions.length">
          <div 
            v-for="(suggestion, index) in suggestions" 
            :key="index"
            class="mb-4 p-4 bg-gray-50 rounded-lg"
          >
            <div class="flex items-start space-x-3">
              <SparklesIcon class="w-5 h-5 text-primary-600 flex-shrink-0 mt-0.5" />
              <div class="flex-1">
                <h4 class="text-sm font-medium text-gray-900 mb-2">
                  {{ suggestion.title }}
                </h4>
                <p class="text-sm text-gray-600">
                  {{ suggestion.content }}
                </p>
                <div class="mt-3 flex items-center space-x-3">
                  <el-button 
                    size="small"
                    @click="handleAction('apply', suggestion)"
                  >
                    应用建议
                  </el-button>
                  <el-button 
                    size="small"
                    text
                    @click="handleAction('ignore', suggestion)"
                  >
                    忽略
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </template>
        <div v-else class="text-center py-8 text-gray-500">
          暂无优化建议
        </div>
      </div>
  
      <template #footer>
        <div class="flex justify-end">
          <el-button @click="visible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { SparklesIcon } from '@heroicons/vue/24/outline'
  
  const props = defineProps({
    modelValue: {
      type: Boolean,
      required: true
    },
    suggestions: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['update:modelValue', 'action'])
  
  const visible = computed({
    get: () => props.modelValue,
    set: (val) => emit('update:modelValue', val)
  })
  
  const handleAction = (type, suggestion) => {
    emit('action', { type, suggestion })
  }
  </script>