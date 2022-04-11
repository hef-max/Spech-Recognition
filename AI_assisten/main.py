from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
from pygame import mixer
import webbrowser
import json
import os


recognizer = speech_recognition.Recognizer()

intents_json = json.loads(open('intents.json').read())

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Go Shopping', 'Clean Room', 'Record Video']

def create_note():
    global recognizer

    speaker.say("What do you want to write into your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I Succesfully created the note {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not undersatnd you! please try again")
            speaker.runAndWait()

def add_todo():
    global recognizer

    speaker.say("What todo you want to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"I added {item} to the todo list")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("i did not understand, please try again")
            speaker.runAndWait()

def show_todos():
    speaker.say("the item on your to do list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def play_music():
    global recognizer


    speaker.say("okey, play to music")
    speaker.runAndWait()

    mixer.init()

    mixer.music.load("Powfu-death-bed.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                sound = recognizer.listen(mic)

                music = recognizer.recognize_google(sound)
                music = music.lower()
                
                if music == intents_json["pause music"]:
                    speaker.say("pause music")
                    speaker.runAndWait()
                    mixer.music.pause()
                elif music == "play music again":
                    speaker.say("okey play music again")
                    speaker.runAndWait()
                    mixer.music.unpause()
                elif music == "stop music":
                    speaker.say("music stop")
                    speaker.runAndWait()
                    mixer.music.stop()
                    break
                break

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I don't understand, please try again")
            speaker.runAndWait()


def browser():
    global recognizer

    speaker.say("apa yang ingin anda cari?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                search = recognizer.recognize_google(audio)
                search = search.lower()

                webbrowser.open(f'https://www.bing.com/search?q={search}')
                done = True

                speaker.say(f"okey, aku akan mencari {search} di browser")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("i did not understand, please try again")
            speaker.runAndWait()


def hello():
    speaker.say("yes sir, what can i do for you")
    speaker.runAndWait()

def name():
    speaker.say("i'am your assisten, my name is lacia")
    speaker.runAndWait()

def open_yt():
    speaker.say("open to youtube")
    speaker.runAndWait()

    webbrowser.open('https://www.youtube.com/')

def quit():
    speaker.say("okey, good bye")
    speaker.runAndWait()
    sys.exit(0)

mappings = {
    'greeting': hello,
    'create_note': create_note,
    'add_todo': add_todo,
    'show_todos': show_todos,
    'exit': quit,
    'music': play_music,
    'name': name,
    'youtube': open_yt,
    'browser': browser,
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()
assistant.save_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            massage = recognizer.recognize_google(audio)
            massage = massage.lower()
        assistant.request(massage)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()