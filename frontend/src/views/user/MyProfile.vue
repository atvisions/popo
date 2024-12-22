<template>
  <div class="min-h-screen bg-gray-50">
    <div class="pb-20">
      <!-- 基本信息卡片 -->
      <div class="bg-white rounded-lg shadow p-4 mb-3 w-full">
        <div class="flex items-start space-x-4 mb-4">
          <!-- 头像部分 -->
          <div class="relative">
            <img 
              :src="getAvatarUrl(resumeData.avatar)" 
              class="w-16 h-16 rounded-full object-cover"
              alt="头像"
              @error="handleImageError"
            />
            <button 
              @click="editModule('basic')"
              class="absolute -bottom-1 -right-1 p-1 bg-primary-600 rounded-full text-white">
              <PencilIcon class="w-3.5 h-3.5" />
            </button>
          </div>
          
          <!-- 用户基本信息 -->
          <div class="flex-1">
            <div class="flex items-center justify-between">
              <h2 class="text-base font-medium">{{ resumeData.name || '未填写姓名' }}</h2>
              <button @click="editModule('basic')" class="text-primary-600">
                <PencilIcon class="w-4 h-4" />
              </button>
            </div>
            
            <!-- 联系信息 -->
            <div class="mt-2 space-y-1.5">
              <div class="flex items-center text-gray-600 text-sm">
                <PhoneIcon class="w-3.5 h-3.5 mr-1.5" />
                <span>{{ resumeData.phone || '未填写联系电话' }}</span>
              </div>
              <div class="flex items-center text-gray-600 text-sm">
                <EnvelopeIcon class="w-3.5 h-3.5 mr-1.5" />
                <span>{{ resumeData.email || '未填写邮箱地址' }}</span>
              </div>
              <div class="flex items-center text-gray-600 text-sm">
                <MapPinIcon class="w-3.5 h-3.5 mr-1.5" />
                <span>{{ resumeData.location || '未填写所在地' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 个人简介 -->
        <div class="mt-3">
          <h3 class="text-sm text-gray-600 mb-1.5">个人简介</h3>
          <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{{ resumeData.bio || '未填写个人简介' }}</p>
        </div>
      </div>

      <!-- 简历状态卡片 -->
      <div class="bg-white rounded-lg shadow p-4 mb-3 w-full">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-800">简历完成度</span>
          <span class="text-sm text-primary-600">{{ completionRate }}%</span>
        </div>
        <div class="h-1 bg-gray-200 rounded-full overflow-hidden mb-3">
          <div 
            class="h-full bg-primary-600 transition-all duration-300"
            :style="{ width: `${completionRate}%` }"
          ></div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <button 
            @click="showAIOptimize"
            class="flex items-center justify-center gap-1 py-2 border border-primary-600 text-primary-600 rounded text-sm hover:bg-primary-200">
            <SparklesIcon class="w-3.5 h-3.5" />
            <span>AI优化</span>
          </button>
          <button 
            @click="importResume"
            class="flex items-center justify-center gap-1 py-2 border border-primary-600 text-primary-600 rounded text-sm hover:bg-primary-200">
            <ArrowUpTrayIcon class="w-3.5 h-3.5" />
            <span>导入</span>
          </button>
          <button 
            @click="previewResume"
            class="flex items-center justify-center gap-1 py-2 border border-primary-600 text-primary-600 rounded text-sm hover:bg-primary-200">
            <EyeIcon class="w-3.5 h-3.5" />
            <span>预览</span>
          </button>
        </div>
      </div>

      <!-- 常规模块列表 -->
      <div class="space-y-3">
        <template v-for="module in activeModules" :key="module.id">
          <div v-if="module.id !== 'basic'" class="bg-white rounded-lg shadow p-4 w-full">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-sm font-medium">{{ module.title }}</h3>
              <div class="flex items-center gap-2">
                <button v-if="module.canAdd" 
                        @click="addItem(module.id)"
                        class="p-1.5 hover:bg-gray-50 rounded">
                  <PlusIcon class="w-4 h-4 text-gray-600" />
                </button>
                <button v-if="module.items?.length" 
                        @click="editModule(module.id)"
                        class="p-1.5 hover:bg-gray-50 rounded">
                  <PencilIcon class="w-4 h-4 text-gray-600" />
                </button>
              </div>
            </div>

            <!-- 模块内容 -->
            <div v-if="module.items?.length" class="space-y-2">
              <div v-for="item in module.items" 
                   :key="item.id"
                   @click="editItem(module.id, item.id)"
                   class="flex items-center justify-between py-2 border-b last:border-0">
                <div>
                  <div class="text-sm">{{ item.title }}</div>
                  <div class="text-xs text-gray-500">{{ item.subtitle }}</div>
                  <div v-if="item.date" class="text-xs text-gray-400">{{ item.date }}</div>
                </div>
                <ChevronRightIcon class="w-4 h-4 text-gray-400" />
              </div>
            </div>

            <!-- 空状态 -->
            <div v-else class="py-3">
              <button @click="addItem(module.id)" 
                      class="w-full py-2 px-4 border border-gray-300 text-gray-600 text-sm text-center rounded">
                添加{{ module.title }}
              </button>
            </div>
          </div>
        </template>
      </div>

      <!-- 添加更多模块 -->
      <div class="bg-white rounded-lg shadow p-4 mt-3 w-full">
        <h3 class="text-sm font-medium mb-3">添加更多模块</h3>
        <div class="grid grid-cols-2 gap-3">
          <button v-for="module in inactiveModules" 
                  :key="module.id"
                  @click="activateModule(module.id)"
                  class="flex items-center gap-2 p-2.5 border hover:border-primary-600 hover:text-primary-600 rounded text-sm">
            <component :is="module.icon" class="w-4 h-4" />
            <span>{{ module.title }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ChevronRightIcon,
  PlusIcon,
  PencilIcon,
  StarIcon,
  LanguageIcon,
  TrophyIcon,
  LinkIcon,
  ArrowUpTrayIcon,
  EyeIcon,
  SparklesIcon,
  PhoneIcon,
  EnvelopeIcon,
  MapPinIcon
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'
import defaultAvatar from '@/assets/images/default-avatar.png'
import { getUserInfo } from '@/api/user'

const router = useRouter()
const loading = ref(false)
const showEditModal = ref(false)
const showAIModal = ref(false)
const currentModule = ref(null)
const currentItem = ref(null)
const aiSuggestions = ref([])
const formData = ref({})

// 媒体服务器地址
const MEDIA_URL = 'http://www.popo.work'

// 处理头像 URL 的函数
const getAvatarUrl = (path) => {
  if (!path) return defaultAvatar
  if (path.startsWith('http')) return path
  return `${MEDIA_URL}${path}`
}

// 处理图片加载错误
const handleImageError = (event) => {
  console.log('Image load failed, falling back to default avatar')
  event.target.src = defaultAvatar
}

// 简历数据
const resumeData = ref({
  name: '',
  email: '',
  phone: '',
  location: '',
  avatar: '',
  bio: '',
  title: '',
  company: '',
  education: ''
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
    id: 'social',
    title: '社交主页',
    active: false,
    icon: LinkIcon,
    canAdd: true,
    items: []
  }
])

// 计算活跃模块
const activeModules = computed(() => {
  return allModules.value.filter(module => module.active)
})

// 计算未激活模块
const inactiveModules = computed(() => {
  return allModules.value.filter(module => !module.active)
})

// 计算简历完成度
const completionRate = computed(() => {
  let total = 0
  let completed = 0
  
  // 检查基本信息
  const basicFields = ['name', 'phone', 'email', 'location', 'bio']
  basicFields.forEach(field => {
    total++
    if (resumeData.value[field]) completed++
  })
  
  // 检查其他模块
  activeModules.value.forEach(module => {
    if (module.required) {
      total++
      if (module.items?.length > 0) completed++
    }
  })
  
  return Math.round((completed / total) * 100)
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
        bio: profileData.bio || '',
        avatar: profileData.avatar || '',
        title: profileData.title || '',
        company: profileData.company || '',
        education: profileData.education || ''
      }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    showToast('获取用户信息失败', 'error')
  } finally {
    loading.value = false
  }
}

// 编辑模块
const editModule = (moduleId) => {
  currentModule.value = allModules.value.find(m => m.id === moduleId)
  if (moduleId === 'basic') {
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

// 导入简历
const importResume = () => {
  showToast('即将开放导入功能', 'info')
}

// 显示AI优化建议
const showAIOptimize = async () => {
  try {
    loading.value = true
    aiSuggestions.value = [
      {
        content: "建议添加更详细的工作经验描述，突出您的具体职责和成就。",
        action: null
      },
      {
        content: "您的技能部分还未完善，建议添加相关专业技能。",
        action: () => activateModule('skills')
      }
    ]
    showAIModal.value = true
  } catch (error) {
    showToast('获取AI建议失败', 'error')
  } finally {
    loading.value = false
  }
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
