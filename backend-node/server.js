const fs = require('fs');
const http = require('http')
const redis = require('redis')
const server = http.createServer(handler).listen(8080)
const io = require('socket.io').listen(server)
const ws = io.of('/websocket')
const sub = redis.createClient(process.env.REDIS_PORT, process.env.REDIS_HOST)
const pub = redis.createClient(process.env.REDIS_PORT, process.env.REDIS_HOST)

function handler(req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'})
  res.end('Hello node!')
}

const PUBLISH_CHANNEL = SUBSCRIBE_CHANNEL =
    process.env.REDIS_SUBSCRIBE_CHANNEL || ''
const EMIT_TARGET_NEW_MESSAGE = 'new_message'
const EMIT_TARGET_EVENT_MESSAGE = 'event_message'
const EMIT_TARGET_CONNECT = 'connect'
const EMIT_TARGET_DISCONNECT = 'disconnect'

function publish_message(channel, message) {
  pub.publish(channel, JSON.stringify(message))
}

function _convert_fmt_message(data) {
  return JSON.parse(data)
}

ws.on('connection', function(socketio) {
  sub.subscribe(SUBSCRIBE_CHANNEL)
  sub.on('message', function(channel, data) {
    console.log('subscribe', channel, data)
    const message = _convert_fmt_message(data)
    socketio.emit(EMIT_TARGET_NEW_MESSAGE, message)
  })

  socketio.on(EMIT_TARGET_CONNECT, function(data) {
    console.log('Connected!')
  })

  socketio.on(EMIT_TARGET_EVENT_MESSAGE, function(message) {
    publish_message(PUBLISH_CHANNEL, message)
  })

  socketio.on(EMIT_TARGET_DISCONNECT, function() {
    console.log('disconnected')
    socketio.emit(
        EMIT_TARGET_EVENT_MESSAGE,
        {'username': 'システム(Node)', 'body': '接続が切れました。'})
    socketio.disconnect()
  })
});
