import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    movieList: []
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
    }
  },
  actions: {
    getMovieList(context, payload) {
      console.log('payload: ', payload)
      context.commit('SAVE_MOVIE_LIST', payload)
    }
  },
  modules: {
  }
})
