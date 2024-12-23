<!-- src/views/user/MyProfile/components/ModuleList.vue -->
<template>
    <div class="space-y-3">
      <div 
        v-for="module in activeModules" 
        :key="module.id"
        class="bg-white rounded-lg shadow"
      >
        <!-- 模块头部 -->
        <div class="p-4 flex items-center justify-between border-b border-gray-200">
          <div class="flex items-center">
            <component 
              :is="module.icon" 
              class="w-5 h-5 text-gray-400 mr-2"
            />
            <h3 class="text-lg font-medium text-gray-900">
              {{ module.name }}
            </h3>
          </div>
          <div class="flex items-center space-x-2">
            <button
              v-if="module.multiple"
              @click="$emit('add', module.id)"
              class="text-primary-600 hover:text-primary-700"
            >
              <PlusIcon class="w-5 h-5" />
            </button>
            <button
              v-if="!module.required"
              @click="$emit('remove', module.id)"
              class="text-gray-400 hover:text-gray-500"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
  
        <!-- 模块内容 -->
        <div class="p-4">
          <template v-if="module.items && module.items.length">
            <div 
              v-for="(item, index) in module.items" 
              :key="index"
              class="flex items-center justify-between py-2"
            >
              <div>
                <div class="font-medium text-gray-900">{{ item.title }}</div>
                <div class="text-sm text-gray-500">{{ item.subtitle }}</div>
              </div>
              <button
                @click="$emit('edit-item', module.id, item)"
                class="text-primary-600 hover:text-primary-700"
              >
                <PencilIcon class="w-4 h-4" />
              </button>
            </div>
          </template>
          <div 
            v-else
            class="text-center py-4"
          >
            <button
              @click="$emit('add', module.id)"
              class="text-primary-600 hover:text-primary-700 text-sm font-medium"
            >
              添加{{ module.name }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import {
    PlusIcon,
    PencilIcon,
    XMarkIcon
  } from '@heroicons/vue/24/outline'
  
  defineProps({
    activeModules: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  })
  
  defineEmits(['add', 'remove', 'edit-item'])
  </script>