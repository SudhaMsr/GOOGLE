import os
from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'demo_service_account.json'
client = texttospeech.TextToSpeechClient()
text_block = ''' Google Text-to-Speech is a cloud service by Google that turns text 
into natural-sounding speech. Using advanced machine learning, it offers a variety of voices and 
languages, making digital content more engaging and accessible to a wide audience.'''

synthesis_input = texttospeech.SynthesisInput(text=text_block)

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",  # Corrected field name
    name='en-US-Standard-C'
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    effects_profile_id=['small-bluetooth-speaker-class-device'],
    speaking_rate=1,
    pitch=1
)

response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)
with open("output.mp3", "wb") as output:
    output.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
