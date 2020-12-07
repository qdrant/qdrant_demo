import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './quasar'
import 'typeface-roboto/index.css';
import ForkMeOnGithub from 'fork-me-on-github-vue';


Vue.use(ForkMeOnGithub);
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
