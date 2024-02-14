from flask import Flask, render_template
import pyttsx3
import threading

app = Flask(__name__)
engine = pyttsx3.init()

def speak(message):
    engine.say(message)
    engine.runAndWait()

def start_tts_thread(message):
    thread = threading.Thread(target=speak, args=(message,))
    thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak/<message>')
def speak_message(message):
    start_tts_thread(message)
    return f'Speaking: {message}'

if __name__ == '__main__':
    app.run(debug=True)
