module.exports = {
  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: false
    }
  },
  transpileDependencies: [
    'quasar'
  ],
  devServer: {
    watchOptions: {
      poll: false
    },
    proxy: {
      "/api/": {
        target: "http://localhost:8000/",
        logLevel: "debug"
      }
    }
  }
}
