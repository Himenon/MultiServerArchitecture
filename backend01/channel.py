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

ns = '/test'

CONN = redis.StrictRedis(
    host=environ.get('REDIS_HOST'),
    port=environ.get('REDIS_PORT'),
    db=environ.get('REDIS_DB'))

CHANNEL = environ.get('REDIS_SUBSCRIBE_CHANNEL')
TARGET_CLIENT_SERVER = 'my_event'
TARGET_BETWEEN_SERVERS = 'mutli_server'


def publish_message(channel, message):
    print("Redis {} にPublishします".format(channel))
    CONN.publish(channel, json.dumps(message))


def subscribe_message(channel):
    print("{}をSubscribeします".format(channel))
    p = CONN.pubsub()
    p.subscribe(channel)
    return p


def format_message(message):
    print(message)
    if isinstance(message['data'], bytes):
        json_data = message['data'].decode('utf-8')
        fmt_data = json.loads(json_data)
        return {'username': fmt_data.get('username'), 'body': fmt_data.get('body')}


def background_thread():
    global TARGET_BETWEEN_SERVERS
    p = subscribe_message(CHANNEL)
    while True:
        socketio.sleep(1)
        recive_msg = p.get_message()
        if recive_msg:
            message = format_message(recive_msg)
            socketio.emit('new_message', message, namespace=ns)


@socketio.on('connect', namespace=ns)
def my_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@socketio.on(TARGET_CLIENT_SERVER, namespace=ns)
def my_message(message):
    print("Clientから受信しました")
    global CHANNEL
    publish_message(CHANNEL, message)
    # emit('server_message', message)


@socketio.on('disconnect', namespace=ns)
def my_disconnect():
    # emit('server_message',
    #      {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()
