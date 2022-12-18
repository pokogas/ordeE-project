import { w3cwebsocket } from 'websocket'
const W3CWebSocket = w3cwebsocket

export const state = () => ({
  websocket: null
})

export const mutations = {
  setWebSocket (state, payload) {
    state.websocket = new W3CWebSocket(`ws://192.168.0.5:81/ws/manage/order/${payload.shopId}?token=${payload.token}`)
  },
  removeWebSocket (state) {
    if (state.websocket !== null) {
      state.websocket.close()
    }
    state.websocket = null
  }
}

export const actions = {
  orderConnection ({ commit }, payload) {
    commit('removeWebSocket')
    commit('setWebSocket', payload)
  },
  orderDisconnect ({ commit }) {
    commit('removeWebSocket')
  }
}
