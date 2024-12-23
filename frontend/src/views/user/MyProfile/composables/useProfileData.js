// src/views/user/MyProfile/composables/useProfileData.js
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import  { API_PATHS } from '@/utils/request'

export function useProfileData() {
  const loading = ref(false)
  const error = ref(null)
  
  // 扩展 resumeData 的初始结构
  const resumeData = ref({
    avatar: '',
    name: '',
    phone: '',
    email: '',
    location: '',
    jobStatus: '',
    workYears: '',
    expectedSalary: '',
    bio: '',
    skills: [],
    education: [],
    experience: []
  })
  
  const formData = ref({})
  const completionRate = ref(0)

  const calculateCompletionRate = () => {
    const requiredFields = ['name', 'phone', 'email', 'location', 'bio']
    const completedFields = requiredFields.filter(field => resumeData.value[field])
    completionRate.value = Math.round((completedFields.length / requiredFields.length) * 100)
  }

  const fetchInitialData = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await request.get('/v1/users/profile/', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })

      if (response.data) {
        // 合并数据，保留现有字段
        resumeData.value = {
          ...resumeData.value,
          ...response.data
        }
        calculateCompletionRate()
      } else {
        throw new Error('Invalid response format')
      }
    } catch (err) {
      console.error('获取数据失败:', err)
      error.value = err
      ElMessage.error('获取个人资料失败，请重试')
    } finally {
      loading.value = false
    }
  }

  const updateResumeData = async (data) => {
    try {
      console.log('准备更新的数据:', data)
  
      // 如果只更新了头像，不需要调用更新接口
      if (Object.keys(data).length === 1 && data.avatar) {
        // 直接更新本地数据
        resumeData.value = {
          ...resumeData.value,
          avatar: data.avatar
        }
        return true
      }
  
      // 构建要发送的数据对象（不包含头像字段）
      const updateData = {
        name: data.name,
        phone: data.phone,
        email: data.email,
        location: data.location,
        bio: data.bio,
        profession: data.profession,
        company: data.company,
        position: data.position
      }
  
      // 移除空值
      Object.keys(updateData).forEach(key => {
        if (updateData[key] === undefined || updateData[key] === null || updateData[key] === '') {
          delete updateData[key]
        }
      })
  
      // 如果没有需要更新的数据，直接返回
      if (Object.keys(updateData).length === 0) {
        return true
      }
  
      console.log('发送到后端的数据:', updateData)
  
      const response = await request.put(API_PATHS.USERS.PROFILE, updateData)
      
      if (response.data && response.data.code === 200) {
        // 更新本地数据
        resumeData.value = {
          ...resumeData.value,
          ...response.data.data
        }
        ElMessage.success('更新成功')
        return true
      }
  
      throw new Error(response.data?.message || '更新失败')
    } catch (error) {
      console.error('更新数据失败:', error)
      ElMessage.error(error.response?.data?.message || error.message || '更新失败')
      throw error
    }
  }

  return {
    loading,
    error,
    resumeData,
    formData,
    completionRate,
    fetchInitialData,
    updateResumeData
  }
}