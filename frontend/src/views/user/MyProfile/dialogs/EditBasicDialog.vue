<!-- src/views/user/MyProfile/dialogs/EditBasicDialog.vue -->
<template>
    <el-dialog
      :model-value="modelValue"
      @update:model-value="$emit('update:modelValue', $event)"
      :width="dialogWidth"
      :close-on-click-modal="false"
      @close="handleClose"
      class="relative"
    >
      <!-- Header -->
      <template #header>
        <div class="border-b border-gray-200 px-6 py-5">
          <h3 class="text-lg font-medium text-gray-900">编辑基本信息</h3>
        </div>
      </template>
  
      <!-- Body -->
      <div class="px-6 py-5">
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- 两列布局 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <!-- 姓名输入框 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">姓名</label>
              <div class="relative">
                <input
                  v-model="form.name"
                  type="text"
                  placeholder="请输入姓名"
                  class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                />
              </div>
            </div>
  
            <!-- 手机号码 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">手机号码</label>
              <input
                v-model="form.phone"
                type="tel"
                placeholder="请输入手机号码"
                class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
              />
            </div>
  
            <!-- 邮箱 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">邮箱</label>
              <input
                v-model="form.email"
                type="email"
                placeholder="请输入邮箱"
                class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
              />
            </div>
  
            <!-- 所在地 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">所在地</label>
              <input
                v-model="form.location"
                type="text"
                placeholder="请输入所在地"
                class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
              />
            </div>
  
            <!-- 求职状态 -->
  <div class="space-y-2">
    <label class="block text-sm font-medium text-gray-700">求职状态</label>
    <Listbox v-model="form.jobStatus">
      <div class="relative">
        <ListboxButton
          class="relative w-full cursor-default rounded-md border border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
        >
          <span class="block truncate">
            {{ jobStatusOptions.find(item => item.value === form.jobStatus)?.label || '请选择求职状态' }}
          </span>
          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </span>
        </ListboxButton>

        <transition
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <ListboxOptions
            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
          >
            <ListboxOption
              v-for="option in jobStatusOptions"
              :key="option.value"
              :value="option.value"
              v-slot="{ active, selected }"
              as="template"
            >
              <li
                :class="[
                  active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                  'relative cursor-default select-none py-2 pl-3 pr-9'
                ]"
              >
                <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                  {{ option.label }}
                </span>
                <span
                  v-if="selected"
                  :class="[
                    active ? 'text-gray-900' : 'text-gray-700',
                    'absolute inset-y-0 right-0 flex items-center pr-4'
                  ]"
                >
                  <CheckIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </li>
            </ListboxOption>
          </ListboxOptions>
        </transition>
      </div>
    </Listbox>
  </div>

  <!-- 工作年限 -->
  <div class="space-y-2">
    <label class="block text-sm font-medium text-gray-700">工作年限</label>
    <Listbox v-model="form.workYears">
      <div class="relative">
        <ListboxButton
          class="relative w-full cursor-default rounded-md border border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
        >
          <span class="block truncate">
            {{ workYearsOptions.find(item => item.value === form.workYears)?.label || '请选择工作年限' }}
          </span>
          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </span>
        </ListboxButton>

        <transition
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <ListboxOptions
            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
          >
            <ListboxOption
              v-for="option in workYearsOptions"
              :key="option.value"
              :value="option.value"
              v-slot="{ active, selected }"
              as="template"
            >
              <li
                :class="[
                  active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                  'relative cursor-default select-none py-2 pl-3 pr-9'
                ]"
              >
                <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                  {{ option.label }}
                </span>
                <span
                  v-if="selected"
                  :class="[
                    active ? 'text-gray-900' : 'text-gray-700',
                    'absolute inset-y-0 right-0 flex items-center pr-4'
                  ]"
                >
                  <CheckIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </li>
            </ListboxOption>
          </ListboxOptions>
        </transition>
      </div>
    </Listbox>
  </div>
           
  
            <!-- 期望薪资 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">期望薪资</label>
              <div class="relative">
                <input
                  v-model="form.expectedSalary"
                  type="text"
                  placeholder="请输入期望薪资"
                  class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 pl-3 pr-12 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                />
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500">
                  元/月
                </span>
              </div>
            </div>
          </div>
  
          <!-- 个人简介 -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">个人简介</label>
            <textarea
              v-model="form.bio"
              :rows="isMobile ? 3 : 4"
              placeholder="请简要介绍一下自己..."
              class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
            ></textarea>
          </div>
        </form>
      </div>
  
      <!-- Footer -->
      <template #footer>
        <div class="border-t border-gray-200 px-6 py-4">
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="handleClose"
              class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-900/10"
            >
              取消
            </button>
            <button
              type="button"
              @click="handleSubmit"
              :disabled="loading"
              class="rounded-md border border-transparent bg-gray-900 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900/10 disabled:opacity-50"
            >
              {{ loading ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </template>
    </el-dialog>
  </template>
 <script setup>
 import { ref, computed, watch } from 'vue'
 import { useWindowSize } from '@vueuse/core'
 import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
 import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'
 
 // 求职状态选项
 const jobStatusOptions = [
   { label: '在职-暂不考虑', value: 'employed_not_looking' },
   { label: '在职-考虑机会', value: 'employed_looking' },
   { label: '离职-正在找工作', value: 'unemployed_looking' },
   { label: '应届生', value: 'fresh_graduate' }
 ]
 
 // 工作年限选项
 const workYearsOptions = [
   { label: '应届生', value: '0' },
   { label: '1年以下', value: '1' },
   { label: '1-3年', value: '2' },
   { label: '3-5年', value: '3' },
   { label: '5-10年', value: '4' },
   { label: '10年以上', value: '5' }
 ]
 
 const { width } = useWindowSize()
 
 // 判断是否为移动端
 const isMobile = computed(() => width.value < 640)
 
 // 根据屏幕宽度设置弹窗宽度
 const dialogWidth = computed(() => {
   if (width.value < 640) return '94%'
   if (width.value < 1024) return '80%'
   return '640px'
 })
 
 const props = defineProps({
   modelValue: {
     type: Boolean,
     default: false
   },
   initialData: {
     type: Object,
     default: () => ({})
   },
   loading: {
     type: Boolean,
     default: false
   }
 })
 
 const emit = defineEmits(['update:modelValue', 'submit'])
 
 const form = ref({
   name: '',
   phone: '',
   email: '',
   location: '',
   jobStatus: '',
   workYears: '',
   expectedSalary: '',
   bio: ''
 })
 
 // 监听初始数据变化
 watch(
   () => props.initialData,
   (newVal) => {
     if (newVal) {
       form.value = { ...newVal }
     }
   },
   { immediate: true }
 )
 
 const handleSubmit = () => {
   emit('submit', form.value)
 }
 
 const handleClose = () => {
   emit('update:modelValue', false)
 }
 </script>