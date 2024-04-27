#!/usr/bin/python3
from requests import post
from json import loads
import pyaudio
import numpy as np
from openwakeword.model import Model
from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
from os import remove

#V----Config----V#

# Global config
language_full = "en-US" # format: en-US

# Home assistant config
server = "http://192.168.xxx.xxx:8123" # http://{your server address}:{your server port}
auth_token = "" # Long lived access token

# Wakeword config
models = ["./hey_house.tflite", "./ok_home.tflite"]
CHANNELS = 1
RATE = 16000
CHUNK = 1280

# Messages
messages = {"SR_UnknownValue": "The speech recognition couldn't understand what you said!", "SR_RequestError": "Could not request results from the speech recognition service!"}

#^----Config-----^#

language = language_full.split("-")[0]

api_headers = {"Authorization": f"Bearer {auth_token}"}

FORMAT = pyaudio.paInt16
audio = pyaudio.PyAudio()
mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
model = Model(wakeword_models=models, inference_framework="tflite")

recognizer = sr.Recognizer()

rate_limit = 50

print("Wake words:")
print(models)
print("-"*30)
print("Listening for a wake word...")

while True:
    audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)
    prediction = model.predict(audio)
    rate_limit += 1
    if rate_limit >= 50:
        for match in prediction.values():
            if match >= 0.3:
                rate_limit = 0

                print("Wake word detected!")
                playsound("./beep.wav")

                with sr.Microphone() as source:
                    print("Listening for text...")
                    sr_audio = recognizer.listen(source)
                
                playsound("./beep.wav")

                try:
                    detected_text = recognizer.recognize_google(sr_audio, language=language_full)
                    print("Detected text:")
                    print(detected_text)
                    print("Sending a request to the home assistant API")

                    api_data = {"text": detected_text, "language": language}
                    api_response = loads(post(server + "/api/conversation/process", json = api_data, headers=api_headers).text)
                    output_text = api_response["response"]["speech"]["plain"]["speech"]

                    print("Request sent!")
                except sr.UnknownValueError:
                    output_text = messages["SR_UnknownValue"]
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    output_text = messages["SR_RequestError"]

                print("Response:")
                print(output_text)
                print("Running TTS")

                gTTS(output_text, lang=language).save("./tts.mp3")
                playsound("./tts.mp3")
                remove("./tts.mp3")

                print("-"*30)
                print("Listening for a wake word...")