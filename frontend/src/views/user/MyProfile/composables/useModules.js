// src/views/user/MyProfile/composables/useModules.js
import { ref, computed } from 'vue'
import { moduleConfig } from '../constants/moduleConfig'

export function useModules() {
  const activeModules = ref([])
  const currentModule = ref(null)
  const currentItem = ref(null)

  const inactiveModules = computed(() => {
    const activeIds = activeModules.value.map(m => m.id)
    return moduleConfig.filter(m => !activeIds.includes(m.id))
  })

  const editModule = (moduleId, item = null) => {
    currentModule.value = activeModules.value.find(m => m.id === moduleId)
    currentItem.value = item
  }

  const addItem = (moduleId) => {
    currentModule.value = activeModules.value.find(m => m.id === moduleId)
    currentItem.value = null
  }

  const removeModule = (moduleId) => {
    const index = activeModules.value.findIndex(m => m.id === moduleId)
    if (index > -1) {
      activeModules.value.splice(index, 1)
    }
  }

  const activateModule = (moduleId) => {
    const module = moduleConfig.find(m => m.id === moduleId)
    if (module) {
      activeModules.value.push({
        ...module,
        items: []
      })
    }
  }

  return {
    activeModules,
    inactiveModules,
    currentModule,
    currentItem,
    editModule,
    addItem,
    removeModule,
    activateModule
  }
}