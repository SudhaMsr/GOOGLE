from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_toggle')
def video_toggle(data):
    emit('toggle_response', data, broadcast=True)

@socketio.on('send_frame')
def send_frame(data):
    emit('receive_frame', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
