import subprocess
from google.cloud import speech

def mp3_to_flac(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-ar", "16000",  # Sample rate of 44.1 kHz
        "-ac", "1",      # Mono audio
        "-compression_level", "3",  # Compression level (0 to 12)
        output_file
    ]
    subprocess.run(command, check=True)

# Function to transcribe speech from FLAC file
def transcribe_audio_flac(file_path, language_code="en-US"):
    client = speech.SpeechClient.from_service_account_file('key.json')

    with open(file_path, "rb") as f:
        audio_data = f.read()

    audio = speech.RecognitionAudio(content=audio_data)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code=language_code
    )

    response = client.recognize(config=config, audio=audio)
    print(response)
    # Print transcriptions
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

# Input and output file paths
input_file = "output.mp3"
output_file = "output.flac"

# Convert MP3 to FLAC
mp3_to_flac(input_file, output_file)

# Transcribe speech from FLAC file
transcribe_audio_flac(output_file)
