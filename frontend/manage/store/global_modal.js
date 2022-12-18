export const state = () => ({
  icon: '',
  title: '',
  message: '',
  isActive: false
})

export const mutations = {
  setIcon (state, icon) {
    state.icon = icon
  },
  setTitle (state, title) {
    state.title = title
  },
  setMessage (state, message) {
    state.message = message
  },
  active (state) {
    state.isActive = true
  },
  deactive (state) {
    state.isActive = false
  }
}

export const actions = {
  openErrorModal ({ commit }, payload) {
    commit('setMessage', payload.message)
    commit('active')
  },
  closeErrorModal ({ commit }) {
    commit('deactive')
    commit('setMessage', '')
  }
}
