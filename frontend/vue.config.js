const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'popo.work'
      return args
    })
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',  // 后端服务器地址
        changeOrigin: true,  // 允许跨域
        ws: true,  // 支持 websocket
        // pathRewrite: {
        //   '^/api': ''  // 如果后端没有/api前缀，可以把/api重写为空
        // }
      }
    }
  }
})
