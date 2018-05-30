import API from '~/api'
import io from 'socket.io-client'

let socket = null

function setWebsocket(socketUrl) {
  socket = io(socketUrl)
}

function listenWebsocket(commit) {
  socket.on('connect', function () {
    socket.emit('my_event', {data: 'I\'m connected'})
  })
  socket.on('new_message', function (msg) {
    console.log("ReceiveMessage")
    if (msg.username && msg.body) {
      commit('setMessage', msg)
    }
  })
}

function sendMessage(message) {
  socket.emit('my_event', message)
}

const state = () => ({
  messages: [
    {
      username: 'user1',
      body: 'こんにちは'
    },
    {
      username: 'user2',
      body: 'こんばんは'
    }
  ]
})

const actions = {
  initializeWebSocket({commit}, payload) {
    console.log("websocketの初期化")
    setWebsocket(payload.socketUrl)
    listenWebsocket(commit)
  },
  sendMessage ({commit}, payload) {
    console.log("sendmeessage")
    sendMessage(payload)
  },
}

const getters = {
}

const mutations = {
  setMessage (state, message) {
    console.log(message)
    state.messages.unshift(message)
  }
}

const computed = {
}

export default {
  namespaced: true,
  state,
  actions,
  getters,
  mutations,
  computed
}
