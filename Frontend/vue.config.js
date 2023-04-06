const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    allowedHosts: "all",
    proxy: {
      '^/api': {
        target: "http://127.0.0.1:5000",
        pathRewrite: { '^/api': '' },
        changeOrigin: true
      }
    }
  },
})
