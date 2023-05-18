import Vue from 'vue'
import VueRouter from 'vue-router'
import SearchView from '@/views/SearchView.vue'
import MovieDetail from '@/views/MovieDetail.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'search',
    component: SearchView
  },
  {
    path: '/detail/:id',
    name: 'movieDetail',
    component: MovieDetail,
    props: true
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
