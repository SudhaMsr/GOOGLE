import cv2
from ocrYolo import detect_objects_and_extract_text
import sys
from flask_socketio import SocketIO
from speech_to_text import speechToText
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import base64
import numpy as np
import time

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('send_text')
def receive_text(text):
    # Process the audio data in Python
    # Example: Convert audio data to base64 for simplicity
    emit('processed_audio', {'result': 'Audio processed successfully', 'text': text})

    # condition depending on text
    if text == "scan":
        emit("speak", "scan activated")
        emit("request_scan")  # start the scan loop: request -> client response -> process -> request
    elif text == "quit scan":
        emit("speak", "scan deactivated")
        emit("deactivate_scan")


# image processing
@socketio.on("video_frame")
def process_image(frame):
    lastTime = time.time()
    decoded_frame = base64.b64decode(frame)
    nparr = np.frombuffer(decoded_frame, np.uint8)

    # Decode the image using OpenCV
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    textPrompt = detect_objects_and_extract_text(img)
    if textPrompt is not None:
        emit("speak", textPrompt)
        print(textPrompt)
    print(time.time() - lastTime)
    emit("request_scan")


if __name__ == '__main__':
    socketio.run(app, debug=True,allow_unsafe_werkzeug=True)
