import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import requests

load_dotenv()

def speak(speech_svc, text):
    speech_svc.say(text)
    speech_svc.runAndWait()

def handle_prompt(speech_svc):
    speak(speech_svc, "Please speak into the microphone and ask your question")
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=20)
        try:
            prompt = recognizer.recognize_google(audio)
            print(f"Question received: {prompt}")
            payload = {
                "prompt": prompt,
                "stream": "false"
            }
            print(f"Sending request to {AGENT_URL}")
            response = requests.post(AGENT_URL, data=payload)
            print(f"Received response {response.json()}")

            answer = response.json().get("response").get("content")
            print(f"answer = {answer}")
            speak(speech_svc, f"The answer is {answer}")
        except sr.UnknownValueError:
            print("Did not understand prompt.")
        except sr.RequestError as e:
            print(f"Error during prompt recognition: {e}")

def listen_for_keyword(speech_svc):
    with sr.Microphone() as source:
        print("Listening for 'Hey Solly'...")

        # Adjust for background noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        running = True
        while running:
            try:
                print("Waiting for Hey Solly...")
                audio = recognizer.listen(source)
                phrase = recognizer.recognize_google(audio).lower()
                #print(f"You said: {phrase}")

                if "hey solly" in phrase or "hey sully" in phrase or "hey sally" in phrase:
                    print(" Entering prompt mode...")
                    handle_prompt(speech_svc)
                if "stop" in phrase or "exit" in phrase:
                    print("Stop word detected. Exiting program...")
                    running = False
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

# Agent Url
AGENT_URL = os.getenv("AGENT_URL")

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set voice properties (optional)
engine.setProperty('rate', 180)     # Speed (default ~200)
engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)

# Make it say something!
speak(engine,"Hello and welcome to AuraWatch..!!!!")

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
listen_for_keyword(engine)
