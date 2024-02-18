from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
import cv2
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_frame')
def handle_video_frame(frame_data):
    try:
        # Decode base64 string to image
        frame_bytes = base64.b64decode(frame_data)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

        if frame is not None and not frame.empty():
            # Process the frame (you can perform any image processing here)

            # Send the processed frame back to the client
            _, encoded_frame = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(encoded_frame).decode('utf-8')
            emit('processed_frame', frame_data)
        else:
            print('Empty or invalid frame received')
    except Exception as e:
        print(f'Error processing frame: {str(e)}')

if __name__ == '__main__':
    socketio.run(app, debug=True)
