from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
from pygame import mixer
import webbrowser
import json

recognizer = speech_recognition.Recognizer()

speaker = tts.init()

def browser():
    global recognizer

    speaker.say("What do you want to search?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                search = recognizer.recognize_google(audio)
                search = search.lower()

                done = True

                speaker.say(f"okey i find {search} to browser")
                speaker.runAndWait()

                webbrowser.open(f'https://www.google.com/{search}/')

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("i did not understand, please try again")
            speaker.runAndWait()