from flask import Flask
from flask_cors import CORS
from api import app as api_app
from channel import socketio

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'
app.register_blueprint(api_app)

if __name__ == '__main__':
    # socketioに登録
    socketio.init_app(app)
    socketio.run(app, port=5000, host='0.0.0.0', debug=True)
