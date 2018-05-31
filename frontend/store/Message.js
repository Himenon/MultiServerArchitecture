import io from 'socket.io-client'
import API from '~/api'

let socket = null

const EMIT_TARGET_EVENT_MESSAGE = 'event_message'

function setWebsocket(socketUrl) {
  socket = io(socketUrl)
}

function listenWebsocket(commit) {
  socket.on('connect', function() {
    console.info('Webscoketの接続を確立しました')
  })
  socket.on('new_message', function(msg) {
    console.log('[new_message]', msg)
    if (msg && ('username' in msg) && ('body' in msg) && msg['username'] &&
        msg['body']) {
      commit('setMessage', msg)
    }
  })
}

function emitMessage(message) {
  socket.emit(EMIT_TARGET_EVENT_MESSAGE, message)
}

const state = () => ({
  messages: [
    {
      username: 'システム(初期メッセージ)',
      body: 'ようこそ。ユーザー名とメッセージを入力して送信してください。'
    },
  ]
})

const actions = {
  initializeWebSocket({commit}, payload) {
    console.log('websocketの初期化')
    setWebsocket(payload.socketUrl)
    listenWebsocket(commit)
  },
  sendMessage({commit}, payload) {
    emitMessage(payload)
  },
}

const getters = {}

const mutations = {
  setMessage(state, message) {
    console.log(message)
    state.messages.unshift(message)
  }
}

const computed = {}

export default {
  namespaced: true, state, actions, getters, mutations, computed
}
