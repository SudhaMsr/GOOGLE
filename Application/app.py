import cv2
# import ocrYolo
import sys
from flask_socketio import SocketIO
from speech_to_text import speechToText
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('send_text')
def receive_text(text):
    # Process the audio data in Python
    # Example: Convert audio data to base64 for simplicity
    print(text)
    emit('processed_audio', {'result': 'Audio processed successfully', 'text': text})
    emit('speak', text)


if __name__ == '__main__':
    socketio.run(app, debug=True)

