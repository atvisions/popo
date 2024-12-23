<!-- src/views/user/MyProfile/dialogs/EditDialog.vue -->
<template>
    <el-dialog
      v-model="visible"
      :title="dialogTitle"
      width="640px"
      :close-on-click-modal="false"
      @close="handleClose"
    >
        <el-form
            ref="formRef"
            :model="formData"
            :rules="currentRules"
            label-width="100px"
            class="py-4"
        >
        <template v-for="field in currentModule?.fields" :key="field.key">
          <!-- 文本输入框 -->
          <el-form-item
            v-if="field.type === 'text'"
            :label="field.label"
            :prop="field.key"
          >
            <el-input
              v-model="formData[field.key]"
              :placeholder="`请输入${field.label}`"
            />
          </el-form-item>
  
          <!-- 文本域 -->
          <el-form-item
            v-else-if="field.type === 'textarea'"
            :label="field.label"
            :prop="field.key"
          >
            <el-input
              v-model="formData[field.key]"
              type="textarea"
              :rows="4"
              :placeholder="`请输入${field.label}`"
            />
          </el-form-item>
  
          <!-- 下拉选择 -->
          <el-form-item
            v-else-if="field.type === 'select'"
            :label="field.label"
            :prop="field.key"
          >
            <el-select
              v-model="formData[field.key]"
              :placeholder="`请选择${field.label}`"
              class="w-full"
            >
              <el-option
                v-for="option in getOptions(field.key)"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>
  
          <!-- 日期选择 -->
          <el-form-item
            v-else-if="field.type === 'date'"
            :label="field.label"
            :prop="field.key"
          >
            <el-date-picker
              v-model="formData[field.key]"
              type="date"
              :placeholder="`请选择${field.label}`"
              class="w-full"
            />
          </el-form-item>
  
          <!-- 日期范围 -->
          <el-form-item
            v-else-if="field.type === 'daterange'"
            :label="field.label"
            :prop="field.key"
          >
            <el-date-picker
              v-model="formData[field.key]"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              class="w-full"
            />
          </el-form-item>
  
          <!-- 标签输入 -->
          <el-form-item
            v-else-if="field.type === 'tags'"
            :label="field.label"
            :prop="field.key"
          >
            <el-select
              v-model="formData[field.key]"
              multiple
              filterable
              allow-create
              default-first-option
              :placeholder="`请输入${field.label}`"
              class="w-full"
            />
          </el-form-item>
        </template>
      </el-form>
  
      <template #footer>
        <div class="flex justify-end space-x-3">
          <el-button @click="handleClose">取消</el-button>
          <el-button 
            type="primary" 
            :loading="loading"
            @click="handleSubmit"
          >
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  import { options } from '../constants/options'
  import { validationRules } from '../constants/rules'
  
  const props = defineProps({
    modelValue: Boolean,
    module: Object,
    initialFormData: Object, // 改名为 initialFormData
    loading: Boolean
})
  // 创建本地表单数据副本
const localFormData = ref({...props.formData})

// 监听 formData 变化
watch(() => props.formData, (newVal) => {
  localFormData.value = {...newVal}
}, { deep: true })
  const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])
  // 创建本地表单数据
const formData = ref({...props.initialFormData})

// 监听初始数据变化
watch(() => props.initialFormData, (newVal) => {
  formData.value = {...newVal}
}, { deep: true })
  const formRef = ref(null)
  const visible = computed({
    get: () => props.modelValue,
    set: (val) => emit('update:modelValue', val)
  })
  
  const currentModule = computed(() => props.module)
  const dialogTitle = computed(() => {
    if (!currentModule.value) return ''
    return `编辑${currentModule.value.name}`
  })
  
  const currentRules = computed(() => {
    if (!currentModule.value) return {}
    return validationRules[currentModule.value.id] || {}
  })
  
  const getOptions = (fieldKey) => {
    return options[fieldKey] || []
  }
  
  const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    emit('submit', formData.value) // 提交本地表单数据
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
  
  const handleClose = () => {
    emit('cancel')
  }
  
  // 监听弹窗关闭，重置表单
  watch(visible, (val) => {
    if (!val && formRef.value) {
      formRef.value.resetFields()
    }
  })
  </script>