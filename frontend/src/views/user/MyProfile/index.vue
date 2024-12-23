<!-- src/views/user/MyProfile/index.vue -->
<template>
    <div class="container mx-auto">
      <div class="max-w-4xl mx-auto space-y-4">
        <!-- 基本信息卡片 -->
        <BasicInfo
        :resumeData="resumeData"
        :loading="loading"
        @update:resumeData="updateResumeData"
        @edit="editBasicInfo"
      />
  
        <!-- 简历状态卡片 -->
        <ResumeStatus
          :completion-rate="completionRate"
          :loading="loading"
          @ai-optimize="showAIOptimize"
          @import="importResume"
          @preview="previewResume"
        />
  
        <!-- 常规模块列表 -->
        <ModuleList
          :active-modules="activeModules"
          :loading="loading"
          @edit="editModule"
          @add="addItem"
          @remove="removeModule"
          @edit-item="editItem"
        />
  
        <!-- 添加更多模块 -->
        <AddModule
          :inactive-modules="inactiveModules"
          :loading="loading"
          @activate="activateModule"
        />
      </div>
  
      <!-- 弹窗组件 -->
      <EditBasicDialog
        v-model="showEditBasicDialog"
        :initial-data="basicFormData"
        :loading="loading"
        @submit="handleBasicSubmit"
      />
  
      <EditDialog
        v-model="showEditModal"
        :module="currentModule"
        :initial-form-data="formData"
        :loading="loading"
        @submit="handleSubmit"
        @cancel="handleCancel"
      />
  
      <AIDialog
        v-model="showAIModal"
        :suggestions="aiSuggestions"
        :loading="loading"
        @action="handleAIAction"
      />
  
      <CreationDialog
        v-model="showCreationModal"
        :selected-ids="selectedCreationIds"
        :loading="loading"
        @submit="handleCreationsSelected"
        @cancel="closeCreationModal"
      />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { ElMessage } from 'element-plus'
  
  // 组件导入
  import BasicInfo from './components/BasicInfo.vue'
  import ResumeStatus from './components/ResumeStatus.vue'
  import ModuleList from './components/ModuleList.vue'
  import AddModule from './components/AddModule.vue'
  import EditDialog from './dialogs/EditDialog.vue'
  import AIDialog from './dialogs/AIDialog.vue'
  import CreationDialog from './dialogs/CreationDialog.vue'
  import EditBasicDialog from './dialogs/EditBasicDialog.vue'
  
  // Composables
  import { useProfileData } from './composables/useProfileData'
  import { useModules } from './composables/useModules'
  import { useDialog } from './composables/useDialog'
  import { useLoading } from './composables/useLoading'
 
  // 初始化各个组合式函数
  const { 
    resumeData, 
    formData, 
    completionRate,
    fetchInitialData,
    updateResumeData 
  } = useProfileData()
  
  const {
    activeModules,
    inactiveModules,
    currentModule,
    editModule,
    addItem,
    removeModule,
    activateModule
  } = useModules()
  
  const {
    showEditModal,
    showAIModal,
    showCreationModal,
    aiSuggestions,
    selectedCreationIds,
    showAIOptimize,
    closeCreationModal,
    handleAIAction
  } = useDialog()
  
  const { loading, withLoading } = useLoading()
  
  // 基本信息编辑状态
  const showEditBasicDialog = ref(false)
  const basicFormData = ref({})
  
  // 打开基本信息编辑
  const editBasicInfo = () => {
    basicFormData.value = {
      name: resumeData.value.name || '',
      phone: resumeData.value.phone || '',
      email: resumeData.value.email || '',
      location: resumeData.value.location || '',
      jobStatus: resumeData.value.jobStatus || '',
      workYears: resumeData.value.workYears || '',
      expectedSalary: resumeData.value.expectedSalary || '',
      bio: resumeData.value.bio || ''
    }
    showEditBasicDialog.value = true
  }
  
  // 处理基本信息提交
  const handleBasicSubmit = async (formData) => {
    try {
      await withLoading(async () => {
        await updateResumeData({ ...resumeData.value, ...formData })
        showEditBasicDialog.value = false
        ElMessage.success('保存成功')
      })
    } catch (error) {
      console.error('保存失败:', error)
      ElMessage.error('保存失败，请稍后重试')
    }
  }
  
  // 生命周期钩子
  onMounted(async () => {
    await withLoading(async () => {
      await fetchInitialData()
    })
  })
  
  // 处理函数
  const handleSubmit = async (formData) => {
    try {
      await withLoading(async () => {
        await updateResumeData(formData)
        showEditModal.value = false
        ElMessage.success('保存成功')
      })
    } catch (error) {
      console.error('保存失败:', error)
      ElMessage.error('保存失败，请检查表单')
    }
  }
  
  const handleCancel = () => {
    showEditModal.value = false
  }
  
  
  const importResume = async () => {
    try {
      await withLoading(async () => {
        // TODO: 实现导入功能
        ElMessage.info('功能开发中')
      })
    } catch (error) {
      console.error('导入失败:', error)
      ElMessage.error('导入失败，请稍后重试')
    }
  }
  
  const previewResume = () => {
    // TODO: 实现预览功能
    ElMessage.info('功能开发中')
  }
  // 处理头像更新

  const handleCreationsSelected = async (selectedIds) => {
    try {
      await withLoading(async () => {
        selectedCreationIds.value = selectedIds
        closeCreationModal()
        ElMessage.success('作品选择成功')
      })
    } catch (error) {
      console.error('作品选择失败:', error)
      ElMessage.error('作品选择失败，请稍后重试')
    }
  }
  
  const editItem = (moduleId, item) => {
    editModule(moduleId)
    formData.value = { ...item }
    showEditModal.value = true
  }
// 初始化数据
onMounted(async () => {
  await fetchInitialData()
})
  </script>