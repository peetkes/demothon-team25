import os
from termios import TCSADRAIN

from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import requests
import sys

load_dotenv()
# Cross platform single-key detection
try:
    import msvcrt
except ImportError:
    import tty
    import termios

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
else:
    def get_key():
        return msvcrt.getch().decode()

def speak(speech_svc, text):
    speech_svc.say(text)
    speech_svc.runAndWait()

# Agent Url
AGENT_URL = os.getenv("AGENT_URL")

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set voice properties (optional)
engine.setProperty('rate', 180)     # Speed (default ~200)
engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)

# Make it say something!
speak(engine,"Hello Team25! Welcome to Solace Agent Mesh..!!!!")
#engine.say("Hello Team25! Welcome to Solace Agent Mesh..!!!!")
#engine.runAndWait()

recognizer = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    recognizer.adjust_for_ambient_noise(source)  # helps with noisy backgrounds
    try:
        while True:
            print("🎤 Please press any key to start and speak into the microphone...")
            speak(engine, "Please press any key to start and and speak into the microphone")
            get_key()
            audio = recognizer.listen(source, 10, 5)
            try:
                text = recognizer.recognize_google(audio)
                print("✅ You said:", text)
                payload = {
                    "prompt": text,
                    "stream": "false"
                }
                print(f"Sending request to {AGENT_URL}")
                response = requests.post(AGENT_URL, data=payload)
                print(f"Received response {response.json()}")

                answer = response.json().get("response").get("content")
                print(f"answer = {answer}")
                speak(engine, answer)

            except sr.UnknownValueError:
                print("❌ Sorry, didn't catch that.")
    except KeyboardInterrupt:
        print("\nExiting... Goodbye!")
        speak(engine, "Goodbye!")