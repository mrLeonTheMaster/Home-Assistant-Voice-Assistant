#!/usr/bin/python3
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("requests")
install("numpy")
install("pyaudio")
install("tflite")
install("tflite-runtime")
install("openwakeword")
install("gTTS")
install("playsound")
install("SpeechRecognition")

import openwakeword

openwakeword.utils.download_models()

print("Setup done!")