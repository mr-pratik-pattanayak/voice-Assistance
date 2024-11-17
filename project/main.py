import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import google.generativeai as genai
import os


recognizer = sr.Recognizer()
engine=pyttsx3.init()
newsApi="ff5695998fa14c5e896bc8eed7e112e3"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts=gTTS(text)
    tts.save("temp.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    genai.configure(api_key="AIzaSyBrMnDV3HcFdnTLbbq6jLJh12UfmDRWoO4")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(command)
    print(response.text)
    return response.text

def processCommand(c):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif c.lower().startswith("play music"):
        song=c.lower.split(" ")[2]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApi}")
        if r.status_code == 200:
            data=r.json()
            articles=data.get("articles",[])
            for article in articles:
                speak(article("title"))
    else:
        output=aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("hi")
    while True:
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("listening...")
                audio = r.listen(source,timeout=5,phrase_time_limit=1)
            word=r.recognize_google(audio)
            if("panda" in word.lower()):
                speak("i'm listening")
                with sr.Microphone() as source:
                    print("panda active")
                    audio = r.listen(source,phrase_time_limit=15)
                    command=r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
