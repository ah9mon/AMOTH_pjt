import Vue from 'vue'
import VueRouter from 'vue-router'
import SearchView from '@/views/SearchView.vue'
import MovieDetail from '@/views/MovieDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ArticleListView from '@/views/ArticleListView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import LoginView from '@/views/LoginView.vue'

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
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: ProfileView,
    props: true
  },
  {
    path: '/article/:id',
    name: 'articleDetail',
    component: ArticleDetailView,
    props: true
  },
  {
    path: '/article',
    name: 'articleList',
    component: ArticleListView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
