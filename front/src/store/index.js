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
    user_id: null,
    profile_picture: null,
  },
  getters: {
    getMovie: (state) => (id) => {
      return state.movieList.find((elem) => elem.id === id)
    } 
  },
  mutations: {
    SAVE_MOVIE_LIST(state, payload) {
      // state.movieList = state.movieList.concat(payload.data)
      for (const movie of payload.data) {
        if (!state.movieList.includes(movie)) {
          state.movieList = state.movieList.concat(movie)
        }
      }
      // state.movieList = state.movieList.concat(payload)
      console.log('payload: ',payload)
      console.log('payload data: ',payload.data)
      console.log(state.movieList)
    },
    SAVE_TOKEN(state, payload) {
      state.token = payload
    },
    DELETE_LOCAL_STORE(state) {
      state.movieList = []
      state.token = null
      state.user_id = null
      state.profile_picture = null
    },
    SAVE_USER_INFO(state, payload) {
      state.user_id = payload.user_id
      state.profile_picture = payload.profile_picture
    }
  },
  actions: {
    getMovieList(context, payload) {
      console.log('payload: ', payload)
      context.commit('SAVE_MOVIE_LIST', payload)
    },
    saveToken(context, payload) {
      context.commit('SAVE_TOKEN', payload)
    },
    deleteLocalStore(context) {
      context.commit('DELETE_LOCAL_STORE')
    },
    saveUserInfo(context, payload) {
      context.commit('SAVE_USER_INFO', payload)
    }
  },
  modules: {
  }
})

export default store