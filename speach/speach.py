import speech_recognition as sr
import pyttsx3
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set voice properties (optional)
engine.setProperty('rate', 180)     # Speed (default ~200)
engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)

# Make it say something!
engine.say("Hello Radisson Hotel Group! Welcome to Solace Agent Mesh..!!!!")
engine.runAndWait()

r = sr.Recognizer()
mic = sr.Microphone()

url = "http://localhost:5050/api/v1/request"

print("🎤 Please speak into the microphone...")

with mic as source:
    r.adjust_for_ambient_noise(source)  # helps with noisy backgrounds
    audio = r.listen(source)

    # while True:
    #    print("🟡 Say something!")
    #    audio = r.listen(source)  # waits until you say something

    try:
        text = r.recognize_google(audio)
        print("✅ You said:", text)
        payload = {
            "prompt": text,
            "stream": "false"
        }
        response = requests.post(url, data=payload)

        print(f"response = {response.json()}")
#        reply = response.get("response").get("content")
#        engine.say(reply)
#        engine.runAndWait()

    except sr.UnknownValueError:
        print("❌ Sorry, didn't catch that.")
