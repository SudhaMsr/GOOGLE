import cv2
# import ocrYolo
import sys
from flask_socketio import SocketIO
from speech_to_text import speechToText
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)

recording_data = []  # Variable to store recorded audio data


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('toggle_microphone')
def toggle_microphone():
    emit('microphone_toggled', {'status': 'Microphone is now {}'.format('On' if len(recording_data) == 0 else 'Off')})


@socketio.on('audio_data')
def handle_audio_data(data):
    audio_data = data.get('audioData')
    recording_data.extend(audio_data)


@socketio.on('send_audio')
def send_audio():
    # Process the audio data in Python
    # Example: Convert audio data to base64 for simplicity
    text = speechToText(recording_data)
    recording_data.clear()

    emit('processed_audio', {'result': 'Audio processed successfully', 'text': text})


if __name__ == '__main__':
    socketio.run(app, debug=True)

