#  Key sk-proj-wGTBXgMfWKWO3pJIptgbT3BlbkFJNThauAO25Izsq2bf7U6S
import speech_recognition as sr
from win32com.client import Dispatch

def speak(text):
    speak = Dispatch("SAPiSpvoice")
    speak.Speak(text)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Could not request results; check your network connection.")
        return ""

import openai

openai.api_key = 'sk-proj-wGTBXgMfWKWO3pJIptgbT3BlbkFJNThauAO25Izsq2bf7U6S'

def ask_openai(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    answer = response.choices[0].text.strip()
    return answer

import os
import webbrowser

def open_program(program_name):
    if program_name.lower() == "notepad":
        os.system("notepad")
    elif program_name.lower() == "calculator":
        os.system("calc")

def open_website(url):
    webbrowser.open(url)

def main():
    while True:
        command = recognize_speech().lower()
        if "open" in command:
            if "notepad" in command or "calculator" in command:
                program_name = "notepad" if "notepad" in command else "calculator"
                speak(f"Opening {program_name}")
                open_program(program_name)
            elif "website" in command:
                url = command.split("website ")[-1]
                speak(f"Opening {url}")
                open_website(url)
        elif "ask" in command:
            question = command.split("ask ")[-1]
            answer = ask_openai(question)
            speak(answer)
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("I am not sure how to help with that.")

if __name__ == "__main__":
    main()
