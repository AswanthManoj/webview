from webview import webview
from time import sleep
import threading
from webview.utils import read_and_encode_mp3

webview.configure(host="localhost", port=8889, debug=True)
webview.start_webview()

import wave 
wave_file = wave.open('output.wav', 'wb')
wave_file.setnchannels(1)  # Mono
wave_file.setsampwidth(2)  # 16-bit samples
wave_file.setframerate(44100)  # Sample rate


def process_audio(audio_bytes):
    #print("Audio data received:", audio_bytes)
    wave_file.writeframes(audio_bytes)


def start_recording():
    webview.start_recording(process_audio)


if __name__ == "__main__":
    
    while True:
        action = input("Enter 'q' to quit: ")
        if(action == "start"):
            start_recording()
        