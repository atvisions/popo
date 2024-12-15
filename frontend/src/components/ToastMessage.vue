<!-- src/components/ToastMessage.vue -->
<template>
  <div v-if="show" 
       class="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 bg-gray-800 text-white px-4 py-2 rounded-md shadow-lg">
    {{ message }}
  </div>
</template>

<script>
export default {
  name: 'ToastMessage',  // 确保组件名与文件名一致
  data() {
    return {
      show: false,
      message: '',
      timer: null
    }
  },
  methods: {
    showMessage(message, duration = 3000) {
      this.message = message
      this.show = true
      
      if (this.timer) {
        clearTimeout(this.timer)
      }
      
      this.timer = setTimeout(() => {
        this.show = false
      }, duration)
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearTimeout(this.timer)
    }
  }
}
</script>