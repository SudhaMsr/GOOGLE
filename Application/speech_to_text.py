from google.cloud import speech
from google.oauth2 import service_account
import base64

LANGUAGE = 'en-US'
CHANNELS = 1
RATE = 48000

credentials = service_account.Credentials.from_service_account_file(
    "resources/Speech_to_Text__API_Service.json")
client = speech.SpeechClient(credentials=credentials)


def speechToText(audio_data):
    # speech to text
    content = base64.b64decode(bytes(audio_data))

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                      sample_rate_hertz=RATE,
                                      language_code=LANGUAGE)
    response = client.recognize(config=config, audio=audio)

    transcribed_text = ""
    print(response.results)
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript + " "

    return transcribed_text

