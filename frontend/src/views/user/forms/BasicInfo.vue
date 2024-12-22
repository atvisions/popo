<template>
    <div class="min-h-screen bg-gray-50">
      <!-- 顶部导航 -->
      <div class="fixed top-0 left-0 right-0 bg-white border-b z-50">
        <div class="flex items-center justify-between px-4 h-14">
          <div class="flex items-center">
            <button class="p-2 -ml-2" @click="goBack">
              <ChevronLeftIcon class="w-6 h-6 text-gray-600" />
            </button>
            <h1 class="text-lg font-medium">在线简历</h1>
          </div>
          <button class="text-primary-600" @click="previewResume">
            预览
          </button>
        </div>
      </div>
  
      <!-- 主要内容区 -->
      <div class="pt-14 pb-20 px-4">
        <!-- 基本信息卡片 -->
        <div class="bg-white rounded-lg p-4 mt-4">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <h2 class="text-xl font-medium">{{ resumeData.name || '添加姓名' }}</h2>
                <button @click="editModule('basic')" class="p-1">
                  <PencilIcon class="w-4 h-4 text-gray-400" />
                </button>
              </div>
              <div class="text-gray-600">{{ resumeData.email || '添加邮箱' }}</div>
              <div class="text-gray-600">{{ resumeData.phone || '添加电话' }}</div>
              <div class="text-gray-500 mt-2">{{ resumeData.location || '添加所在地' }}</div>
            </div>
            <div class="relative">
              <img 
                :src="resumeData.avatar || defaultAvatar" 
                class="w-16 h-16 rounded-full object-cover"
                alt="头像" 
              />
              <button 
                @click="editModule('basic')"
                class="absolute -bottom-1 -right-1 p-1.5 bg-primary-600 rounded-full text-white">
                <PencilIcon class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
  
        <!-- 常规模块列表 -->
        <div class="space-y-4 mt-4">
          <template v-for="module in activeModules" :key="module.id">
            <div class="bg-white rounded-lg p-4">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-medium">{{ module.title }}</h3>
                <div class="flex items-center gap-2">
                  <button v-if="module.canAdd" 
                          @click="addItem(module.id)"
                          class="p-2 hover:bg-gray-50 rounded-full">
                    <PlusIcon class="w-5 h-5 text-gray-600" />
                  </button>
                  <button v-if="module.items?.length" 
                          @click="editModule(module.id)"
                          class="p-2 hover:bg-gray-50 rounded-full">
                    <PencilIcon class="w-5 h-5 text-gray-600" />
                  </button>
                </div>
              </div>
  
              <!-- 模块内容 -->
              <div v-if="module.items?.length" class="space-y-3">
                <div v-for="item in module.items" 
                     :key="item.id"
                     @click="editItem(module.id, item.id)"
                     class="flex items-center justify-between py-3 border-b last:border-0">
                  <div>
                    <div class="font-medium">{{ item.title }}</div>
                    <div class="text-gray-500">{{ item.subtitle }}</div>
                    <div v-if="item.date" class="text-gray-400 text-sm">{{ item.date }}</div>
                  </div>
                  <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                </div>
              </div>
  
              <!-- 空状态 -->
              <div v-else class="py-4">
                <button @click="addItem(module.id)" 
                        class="w-full py-2 px-4 border border-gray-300 rounded-lg text-gray-600 text-center">
                  添加{{ module.title }}
                </button>
              </div>
            </div>
          </template>
        </div>
  
        <!-- 添加更多模块 -->
        <div class="bg-white rounded-lg p-4 mt-4">
          <h3 class="text-lg font-medium mb-4">添加更多模块</h3>
          <div class="grid grid-cols-2 gap-4">
            <button v-for="module in inactiveModules" 
                    :key="module.id"
                    @click="activateModule(module.id)"
                    class="flex items-center gap-2 p-3 border rounded-lg hover:border-primary-600 hover:text-primary-600">
              <component :is="module.icon" class="w-5 h-5" />
              <span>{{ module.title }}</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- 底部工具栏 -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t px-4 py-3">
        <button class="w-full py-3 gradient-bg text-white rounded-lg font-medium">
          生成简历
        </button>
      </div>
  
      <!-- 编辑弹窗 -->
      <div v-if="showEditModal" 
           class="fixed inset-0 bg-black bg-opacity-50 z-50"
           @click="closeEditModal">
        <div class="absolute bottom-0 left-0 right-0 bg-white rounded-t-xl max-h-[90vh] overflow-y-auto" 
             @click.stop>
          <!-- 弹窗头部 -->
          <div class="sticky top-0 bg-white border-b px-4 py-3 flex items-center justify-between">
            <h3 class="text-lg font-medium">编辑{{ currentModule?.title }}</h3>
            <button @click="closeEditModal">
              <XMarkIcon class="w-6 h-6 text-gray-400" />
            </button>
          </div>
  
          <!-- 基本信息编辑表单 -->
          <div v-if="currentModule?.id === 'basic'" class="p-4 space-y-4">
            <!-- 头像上传 -->
            <div class="flex items-center space-x-4">
              <div class="relative">
                <img :src="formData.avatar || defaultAvatar" 
                     class="w-20 h-20 rounded-full object-cover"
                     alt="头像" />
                <input type="file"
                       ref="avatarInput"
                       class="hidden"
                       accept="image/*"
                       @change="handleAvatarUpload" />
                <button @click="triggerFileInput"
                        class="absolute bottom-0 right-0 p-1.5 bg-primary-600 rounded-full text-white">
                  <PencilIcon class="w-4 h-4" />
                </button>
              </div>
              <div class="flex-1">
                <label class="block text-sm font-medium text-gray-700">头像</label>
                <p class="text-sm text-gray-500">建议使用正方形图片</p>
              </div>
            </div>
  
            <!-- 基本信息表单字段 -->
            <div v-for="field in basicFields" :key="field.key" class="space-y-1">
              <label class="block text-sm font-medium text-gray-700">{{ field.label }}</label>
              <input v-if="field.type !== 'textarea'"
                     :type="field.type"
                     v-model="formData[field.key]"
                     class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500" />
              <textarea v-else
                       v-model="formData[field.key]"
                       rows="4"
                       class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"></textarea>
            </div>
          </div>
  
          <!-- 保存按钮 -->
          <div class="sticky bottom-0 bg-white border-t p-4">
            <button @click="saveChanges"
                    :disabled="loading"
                    class="w-full py-3 gradient-bg text-white rounded-lg font-medium disabled:opacity-50">
              {{ loading ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  import { 
    ChevronLeftIcon,
    ChevronRightIcon,
    PlusIcon,
    PencilIcon,
    XMarkIcon,
    StarIcon,
    LanguageIcon,
    TrophyIcon,
    LinkIcon
  } from '@heroicons/vue/24/outline'
  import { showToast } from '@/components/ToastMessage'
  import defaultAvatar from '@/assets/images/default-avatar.png'
  import { updateUserInfo, uploadAvatar, getUserInfo } from '@/api/user'
  
  const store = useStore()
  const router = useRouter()
  const avatarInput = ref(null)
  const loading = ref(false)
  const showEditModal = ref(false)
  const currentModule = ref(null)
  const currentItem = ref(null)
  
  // 基本信息表单字段配置
  const basicFields = [
    { key: 'name', label: '姓名', type: 'text' },
    { key: 'phone', label: '联系电话', type: 'tel' },
    { key: 'email', label: '联系邮箱', type: 'email' },
    { key: 'location', label: '所在地', type: 'text' },
    { key: 'bio', label: '个人简介', type: 'textarea' }
  ]
  
  // 简历数据
  const resumeData = ref({
    name: '',
    email: '',
    phone: '',
    location: '',
    avatar: '',
    bio: ''
  })
  
  // 表单数据
  const formData = ref({
    name: '',
    avatar: '',
    phone: '',
    email: '',
    location: '',
    bio: ''
  })
  
  // 所有模块配置
  const allModules = ref([
    {
      id: 'basic',
      title: '基本信息',
      active: true,
      required: true
    },
    {
      id: 'jobPreference',
      title: '求职意向',
      active: true,
      required: true,
      canAdd: true,
      items: []
    },
    {
      id: 'education',
      title: '教育经历',
      active: true,
      required: true,
      canAdd: true,
      items: []
    },
    {
      id: 'experience',
      title: '工作经验',
      active: true,
      required: true,
      canAdd: true,
      items: []
    },
    {
      id: 'projects',
      title: '项目经验',
      active: true,
      canAdd: true,
      items: []
    },
    {
      id: 'skills',
      title: '技能特长',
      active: false,
      icon: StarIcon,
      canAdd: true,
      items: []
    },
    {
      id: 'languages',
      title: '语言能力',
      active: false,
      icon: LanguageIcon,
      canAdd: true,
      items: []
    },
    {
      id: 'certificates',
      title: '证书奖项',
      active: false,
      icon: TrophyIcon,
      canAdd: true,
      items: []
    },
    {
      id: 'links',
      title: '社交主页',
      active: false,
      icon: LinkIcon,
      canAdd: true,
      items: []
    }
  ])
  
  // 计算活跃的模块
  const activeModules = computed(() => {
    return allModules.value.filter(m => m.active)
  })
  
  // 计算未激活的模块
  const inactiveModules = computed(() => {
    return allModules.value.filter(m => !m.active && !m.required)
  })
  
  // 获取用户信息
  const fetchUserProfile = async () => {
    try {
      loading.value = true
      const response = await getUserInfo()
      
      if (response.data.code === 200) {
        const profileData = response.data.data
        resumeData.value = {
          name: profileData.name || '',
          email: profileData.email || '',
          phone: profileData.phone || '',
          location: profileData.location || '',
          avatar: profileData.avatar || '',
          bio: profileData.bio || ''
        }
        // 同步到表单数据
        Object.assign(formData.value, resumeData.value)
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
      showToast('获取用户信息失败', 'error')
    } finally {
      loading.value = false
    }
  }
  
  // 处理头像上传
  const handleAvatarUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return
  
    const isImage = file.type.startsWith('image/')
    const isLt2M = file.size / 1024 / 1024 < 2
  
    if (!isImage) {
      showToast('请上传图片文件', 'error')
      return
    }
  
    if (!isLt2M) {
      showToast('图片大小不能超过 2MB', 'error')
      return
    }
  
    try {
      loading.value = true
      const avatarFormData = new FormData()
      avatarFormData.append('avatar', file)
  
      const response = await uploadAvatar(avatarFormData)
      
      if (response.data.code === 200) {
        const newAvatarUrl = response.data.data.avatar
        formData.value.avatar = newAvatarUrl
        resumeData.value.avatar = newAvatarUrl
        showToast('头像上传成功', 'success')
      }
    } catch (error) {
      console.error('头像上传失败:', error)
      showToast(error.response?.data?.message || '头像上传失败', 'error')
    } finally {
      if (avatarInput.value) {
        avatarInput.value.value = ''
      }
      loading.value = false
    }
  }
  
  // 触发文件选择
  const triggerFileInput = () => {
    avatarInput.value?.click()
  }
  
  // 保存修改
  const saveChanges = async () => {
    if (loading.value) return
  
    try {
      loading.value = true
      const response = await updateUserInfo(formData.value)
      
      if (response.data.code === 200) {
        Object.assign(resumeData.value, response.data.data)
        store.commit('SET_USER_INFO', response.data.data)
        showToast('保存成功', 'success')
        closeEditModal()
      }
    } catch (error) {
      console.error('保存失败:', error)
      showToast(error.response?.data?.message || '保存失败', 'error')
    } finally {
      loading.value = false
    }
  }
  
  // 编辑模块
  const editModule = (moduleId) => {
    currentModule.value = allModules.value.find(m => m.id === moduleId)
    if (moduleId === 'basic') {
      // 编辑基本信息时，同步当前数据到表单
      Object.assign(formData.value, resumeData.value)
    }
    showEditModal.value = true
  }
  
  // 添加条目
  const addItem = (moduleId) => {
    currentModule.value = allModules.value.find(m => m.id === moduleId)
    currentItem.value = null
    showEditModal.value = true
  }
  
  // 编辑条目
  const editItem = (moduleId, itemId) => {
    currentModule.value = allModules.value.find(m => m.id === moduleId)
    currentItem.value = currentModule.value.items.find(item => item.id === itemId)
    showEditModal.value = true
  }
  
  // 激活模块
  const activateModule = (moduleId) => {
    const module = allModules.value.find(m => m.id === moduleId)
    if (module) {
      module.active = true
    }
  }
  
  // 关闭编辑弹窗
  const closeEditModal = () => {
    showEditModal.value = false
    currentModule.value = null
    currentItem.value = null
  }
  
  // 返回上一页
  const goBack = () => {
    router.back()
  }
  
  // 预览简历
  const previewResume = () => {
    router.push('/resume/preview')
  }
  
  // 生命周期钩子
  onMounted(() => {
    fetchUserProfile()
  })
  </script>
  <style scoped>
  .gradient-bg {
    background: linear-gradient(to right, var(--primary-500), var(--primary-600));
  }
  </style>