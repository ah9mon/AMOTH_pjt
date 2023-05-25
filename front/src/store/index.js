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
    databaseList: [],
    initialMovie: null,
    token: null,
    source: null,
    user_id: null,
    profile_picture: null,
    darkmode: true
  },
  getters: {
    getFromMovieList: (state) => (id) => {
      return state.movieList.find((elem) => elem.id === id)
    },
    getFromDatabaseList: (state) => (id) => {
      return state.databaseList.find((elem) => elem.id === id)
    },
    getFromInitialMovie(state) {
      return state.initialMovie
    },
  },
  mutations: {
    UPDATE_MOVIE_LIST(state, payload) {
      // state.movieList = state.movieList.concat(payload.data)
      for (const movie of payload) {
        let isNew = true
        for (const movieKey in state.movieList) {
          if (state.movieList[movieKey].movie_id === movie.movie_id) {
            isNew = false
            state.movieList[movieKey].reason = movie.reason
            break
          }
        }
        if (isNew) {
          // state.movieList = state.movieList.concat(movie)
          state.movieList.splice(0, 0, movie)
        }
      }
    },
    UPDATE_DATABASE_LIST(state, payload) {
      for (const movie of payload) {
        let isNew = true
        for (const movieKey in state.databaseList) {
          if (state.databaseList[movieKey].movie_id === movie.movie_id) {
            isNew = false
          }
        }
        if (isNew) {
          state.databaseList.splice(0, 0, movie)
        }
      }
    },
    SAVE_TOKEN(state, payload) {
      state.token = payload
    },
    SAVE_SOURCE(state, payload) {
      state.source = payload
    },
    DELETE_LOCAL_STORE(state) {
      console.log('logout and cleared local storage')
      state.movieList = []
      state.databaseList = []
      state.initialMovie = null
      state.token = null
      state.source = null
      state.user_id = null
      state.profile_picture = null
    },
    SAVE_USER_INFO(state, payload) {
      state.user_id = payload.user_id
      state.profile_picture = payload.profile_picture
    },
    TOGGLE_DARK_MODE(state, payload) {
      state.darkmode = payload
    },
    UPDATE_INITIAL_MOVIE(state, payload) {
      state.initialMovie = payload
    }
  },
  actions: {
    updateMovieList(context, payload) {
      context.commit('UPDATE_MOVIE_LIST', payload)
    },
    updateDatabaseList(context, payload) {
      context.commit('UPDATE_DATABASE_LIST', payload)
    },
    saveToken(context, payload) {
      context.commit('SAVE_TOKEN', payload)
    },
    saveSource(context, payload) {
      context.commit('SAVE_SOURCE', payload)
    },
    deleteLocalStore(context) {
      context.commit('DELETE_LOCAL_STORE')
    },
    saveUserInfo(context, payload) {
      context.commit('SAVE_USER_INFO', payload)
    },
    toggleDarkMode(context, payload) {
      context.commit('TOGGLE_DARK_MODE', payload)
    },
    updateInitialMovie(context, payload) {
      context.commit('UPDATE_INITIAL_MOVIE', payload)
    }
  },
  modules: {
  }
})

export default store