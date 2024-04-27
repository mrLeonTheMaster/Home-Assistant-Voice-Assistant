#!/usr/bin/python3
import subprocess
import sys

def pip_install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

password = input("Enter your sudo password: ")

pip_install("requests")
pip_install("numpy")
pip_install("tflite")
pip_install("tflite-runtime")
pip_install("openwakeword")
pip_install("gTTS")
pip_install("playsound")
pip_install("SpeechRecognition")

subprocess.check_call(["echo", "'" + password + "'", "|", "sudo", "-S", "apt", "install", "-y", "portaudio19-dev"])

pip_install("pyaudio")

print("Setup done!")
