from flask import Flask, render_template, Response
import cv2
import annotate_realtime
import ocrYolo
import sys
from flask_socketio import SocketIO


app = Flask(__name__)
# socketio = SocketIO(app)


def gen_frames():
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or replace with the video file path

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = ocrYolo.detect_objects_and_extract_text(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
