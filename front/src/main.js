import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import InfiniteLoading from 'vue-infinite-loading'
import '@/styles/layouts.scss'

Vue.config.productionTip = false
Vue.use(InfiniteLoading, {})

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
