import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

const store = new Vuex.Store({
  plugins: [
    createPersistedState()
  ],
  state: {
    movieList: [],
    token: null,
  },
  getters: {
    getMovie: (state) => (id) => {
      return state.movieList.find((elem) => elem.id === id)
    } 
  },
  mutations: {
    SAVE_MOVIE_LIST(state, payload) {
      state.movieList = state.movieList.concat(payload)
      console.log(payload)
      console.log(state.movieList)
    },
    SAVE_TOKEN(state, payload) {
      state.token = payload
    }
  },
  actions: {
    getMovieList(context, payload) {
      console.log('payload: ', payload)
      context.commit('SAVE_MOVIE_LIST', payload)
    },
    saveToken(context, payload) {
      context.commit('SAVE_TOKEN', payload)
    }
  },
  modules: {
  }
})

export default store