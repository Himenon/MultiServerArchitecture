from threading import Lock
from flask_socketio import emit, disconnect
from flask import request, session
from flask_socketio import SocketIO
import redis
from os import environ
from logging import getLogger
import json
logger = getLogger(__name__)

socketio = SocketIO()
thread = None
thread_lock = Lock()

# WebSocketの接続先ネームスペースを用意
# http://localhost:5000/websocket
WS_NAMESPACE = '/websocket'

CONN = redis.StrictRedis(
    host=environ.get('REDIS_HOST'),
    port=environ.get('REDIS_PORT'),
    db=environ.get('REDIS_DB'))

PUBLISH_CHANNEL = SUBSCRIBE_CHANNEL = environ.get('REDIS_SUBSCRIBE_CHANNEL')
EMIT_TARGET_NEW_MESSAGE = 'new_message'
EMIT_TARGET_EVENT_MESSAGE = 'event_message'


def publish_message(channel, message):
    """
    シリアライズ化して送信
    """
    CONN.publish(channel, json.dumps(message))


def subscribe_message(channel):
    p = CONN.pubsub()
    p.subscribe(channel)
    return p

def background_thread():
    global SUBSCRIBE_CHANNEL
    p = subscribe_message(SUBSCRIBE_CHANNEL)

    def _convert_fmt_message(data):
        # デシリアライズ化する
        _fmt_data = json.loads(data.decode('utf-8'))
        return {'username': _fmt_data.get('username'), 'body': _fmt_data.get('body')}

    while True:
        socketio.sleep(0.01)
        _rcv_msg = p.get_message()
        if not _rcv_msg:
            continue
        _data = _rcv_msg['data']
        if not isinstance(_data, bytes):
            continue
        message = _convert_fmt_message(_data)
        socketio.emit(EMIT_TARGET_NEW_MESSAGE, message, namespace=ns)        


@socketio.on('connect', namespace=WS_NAMESPACE)
def connect_to_client():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@socketio.on(EMIT_TARGET_EVENT_MESSAGE, namespace=WS_NAMESPACE)
def save_message(message):
    global PUBLISH_CHANNEL
    # TODO メッセージの永続化
    publish_message(PUBLISH_CHANNEL, message)


@socketio.on('disconnect', namespace=WS_NAMESPACE)
def my_disconnect():
    global EMIT_TARGET_EVENT_MESSAGE
    emit(EMIT_TARGET_EVENT_MESSAGE, {'username': 'システム', 'body': '接続が切れました。'})
    disconnect()
