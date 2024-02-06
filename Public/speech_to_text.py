from google.cloud import speech
from google.oauth2 import service_account
import pyaudio
import keyboard

LANGUAGE = 'en-US'
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

credentials = service_account.Credentials.from_service_account_file(
    "../Forest/API_keys/Speech_to_Text__API_Service.json")
client = speech.SpeechClient(credentials=credentials)


def speechToText():

    # wait for pressing key 'r', record, speech-to-text

    frames = []
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    keyboard.wait('r')

    while keyboard.is_pressed('r'):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # speech to text
    content = b''.join(frames)
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                      sample_rate_hertz=RATE,
                                      language_code=LANGUAGE)
    results = client.recognize(config=config, audio=audio).results
    if not results:
        return None
    else:
        return results[0].alternatives[0].transcript


if __name__ == '__main__':
    print(speechToText())
