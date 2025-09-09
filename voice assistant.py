
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import sys

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
else:
    print(" No voices found for TTS engine.")

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def greet():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        speak("Good morning!")
    elif current_hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def tell_time():
    now = datetime.datetime.now().strftime("%H:%M")
    speak(f"The current time is {now}")

def tell_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {today}")

def search_web(query):
    speak(f"Searching the web for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_command():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
    except sr.WaitTimeoutError:
        speak("Listening timed out. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Speech service is unavailable.")
    except OSError:
        speak("Microphone not accessible.")
    return ""

def handle_command(command):
    if "hello" in command:
        greet()
    elif "time" in command:
        tell_time()
    elif "date" in command:
        tell_date()
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            search_web(query)
        else:
            speak("What would you like me to search for?")
    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        sys.exit()
    else:
        speak("Sorry, I don't understand that command.")

def main():
    speak("Voice assistant activated. Say 'hello' to begin.")
    while True:
        command = get_command()
        if command:
            handle_command(command)

if __name__ == "__main__":
    main()