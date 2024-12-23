<!-- src/views/user/MyProfile/components/BasicInfo.vue -->
<template>
    <div class="bg-white rounded-lg shadow">
      <div class="p-4">
        <div class="flex items-start space-x-5">
          <!-- 头像部分 -->
          <div class="relative group">
            <img 
                :src="avatarUrl" 
                class="w-20 h-20 rounded-full object-cover border-2 border-white shadow"
                alt="用户头像"
                @error="handleImageError"
                />
                <div 
                @click="triggerUpload"
                class="absolute inset-0 flex items-center justify-center rounded-full bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity duration-200"
                >
                <CameraIcon class="w-8 h-8 text-white" />
                </div>
                <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleFileChange"
                />
          </div>
  
          <!-- 用户信息 -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-3">
              <h2 class="text-lg font-medium text-gray-900">
                <template v-if="resumeData.name">
                  {{ resumeData.name }}
                </template>
                <span v-else class="text-sm text-gray-400">未设置姓名</span>
              </h2>
              <button
                @click="$emit('edit')"
                class="inline-flex items-center px-2.5 py-1 text-xs font-medium text-primary-600 hover:text-primary-700 border border-primary-600 hover:border-primary-700 rounded"
              >
                <PencilIcon class="w-3.5 h-3.5 mr-1" />
                编辑资料
              </button>
            </div>
  
            <!-- 基本信息列表 -->
            <div class="grid grid-cols-2 gap-3">
              <!-- 手机号 -->
              <div class="flex items-center text-gray-600">
                <PhoneIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <template v-if="resumeData.phone">
                  <span class="text-sm truncate">{{ resumeData.phone }}</span>
                </template>
                <span v-else class="text-sm text-gray-400 truncate">未设置手机号</span>
              </div>
  
              <!-- 邮箱 -->
              <div class="flex items-center text-gray-600">
                <EnvelopeIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <template v-if="resumeData.email">
                  <span class="text-sm truncate">{{ resumeData.email }}</span>
                </template>
                <span v-else class="text-sm text-gray-400 truncate">未设置邮箱</span>
              </div>
  
              <!-- 所在地 -->
              <div class="flex items-center text-gray-600">
                <MapPinIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <template v-if="resumeData.location">
                  <span class="text-sm truncate">{{ resumeData.location }}</span>
                </template>
                <span v-else class="text-sm text-gray-400 truncate">未设置所在地</span>
              </div>
  
              <!-- 求职状态 -->
              <div class="flex items-center text-gray-600">
                <BriefcaseIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <template v-if="resumeData.jobStatus">
                  <span class="text-sm truncate">{{ resumeData.jobStatus }}</span>
                </template>
                <span v-else class="text-sm text-gray-400 truncate">未设置求职状态</span>
              </div>
  
              <!-- 工作年限 -->
              <div class="flex items-center text-gray-600">
                <ClockIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <template v-if="resumeData.workYears">
                  <span class="text-sm truncate">{{ resumeData.workYears }}</span>
                </template>
                <span v-else class="text-sm text-gray-400 truncate">未设置工作年限</span>
              </div>
  
              <!-- 期望薪资 -->
              <div class="flex items-center text-gray-600">
                <CurrencyYenIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <template v-if="resumeData.expectedSalary">
                  <span class="text-sm truncate">{{ resumeData.expectedSalary }}</span>
                </template>
                <span v-else class="text-sm text-gray-400 truncate">未设置期望薪资</span>
              </div>
            </div>
  
            <!-- 个人简介 -->
            <div class="mt-3">
              <div class="flex items-center text-gray-600 mb-1">
                <DocumentTextIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <span class="text-sm font-medium">个人简介</span>
              </div>
              <template v-if="resumeData.bio">
                <p class="text-sm text-gray-600 leading-relaxed line-clamp-2">
                  {{ resumeData.bio }}
                </p>
              </template>
              <p v-else class="text-sm text-gray-400 leading-relaxed">
                未设置个人简介
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref, computed } from 'vue'
import { ElMessage , ElLoading } from 'element-plus'
import request, { API_PATHS } from '@/utils/request'  
import defaultAvatarImage from '@/assets/images/default-avatar.png'
import { useStore } from 'vuex'
const store = useStore()
const loadingInstance = ref(null)
import {
  PencilIcon,
  PhoneIcon,
  EnvelopeIcon,
  MapPinIcon,
  BriefcaseIcon,
  ClockIcon,
  CurrencyYenIcon,
  DocumentTextIcon,
  CameraIcon
} from '@heroicons/vue/24/outline'
// 从 store 获取头像
const avatarUrl = computed(() => store.getters.getUserAvatar)
// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = defaultAvatarImage
}
const props = defineProps({
  resumeData: {
    type: Object,
    required: true
  },
  loading: Boolean
})

const emit = defineEmits(['update:resumeData'])
const fileInput = ref(null)

// 处理文件上传
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 文件类型验证
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    ElMessage.error('请上传 JPG、PNG 或 GIF 格式的图片')
    event.target.value = ''
    return
  }

  // 文件大小验证 (5MB)
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    ElMessage.error('图片大小不能超过 5MB')
    event.target.value = ''
    return
  }

  // 图片尺寸验证
  try {
    await new Promise((resolve, reject) => {
      const img = new Image()
      img.src = URL.createObjectURL(file)
      img.onload = () => {
        URL.revokeObjectURL(img.src)
        // 最小尺寸要求：100x100
        if (img.width < 100 || img.height < 100) {
          reject(new Error('图片尺寸太小，请上传至少 100x100 像素的图片'))
          return
        }
        // 最大尺寸要求：4000x4000
        if (img.width > 4000 || img.height > 4000) {
          reject(new Error('图片尺寸太大，请上传不超过 4000x4000 像素的图片'))
          return
        }
        resolve()
      }
      img.onerror = () => reject(new Error('图片加载失败，请重试'))
    })
  } catch (error) {
    ElMessage.error(error.message)
    event.target.value = ''
    return
  }

  // 准备上传数据
  const formData = new FormData()
  formData.append('avatar', file)

  try {
    // 显示上传中提示
    loadingInstance.value = ElLoading.service({
      lock: true,
      text: '头像上传中...',
      background: 'rgba(0, 0, 0, 0.7)'
    })

    const response = await request.post(API_PATHS.USERS.AVATAR, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    if (response.data && response.data.code === 200) {
      const avatarPath = response.data.data.avatar
      // 只更新 store 中的用户信息
      store.commit('SET_USER_INFO', {
        data: {
          avatar: avatarPath
        }
      })
      // 更新本地数据
      emit('update:resumeData', {
        ...props.resumeData,
        avatar: avatarPath
      })

     ElMessage.success('头像上传成功')
    } else {
      throw new Error(response.data?.message || '上传失败')
    }
  } catch (error) {
    console.error('头像上传失败:', error)
    ElMessage.error(error.message || '头像上传失败，请重试')
  } finally {
    // 关闭加载提示
    loadingInstance.value?.close()
    loadingInstance.value = null
    // 清空文件输入框
    event.target.value = ''
  }
}


// 触发文件选择
const triggerUpload = () => {
  fileInput.value.click()
}
</script>