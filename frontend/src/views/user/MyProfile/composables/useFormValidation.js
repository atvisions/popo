// src/views/user/MyProfile/composables/useFormValidation.js
import { ref } from 'vue'
import { validationRules } from '../constants/rules'

export function useFormValidation() {
  const formRef = ref(null)

  const validateForm = async () => {
    if (!formRef.value) return true
    try {
      await formRef.value.validate()
      return true
    } catch (error) {
      return false
    }
  }

  const resetValidation = () => {
    if (formRef.value) {
      formRef.value.resetFields()
    }
  }

  return {
    formRef,
    validationRules,
    validateForm,
    resetValidation
  }
}