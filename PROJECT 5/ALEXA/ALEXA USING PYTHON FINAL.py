import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys


# Initialize recognizer and engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Get available voices (optional)
voices = engine.getProperty('voices')

# Function to choose voice (optional)
def choose_voice():
    if len(voices) > 1:
        for i, voice in enumerate(voices):
            print(f"Voice {i+1}: {voice.name}")
        choice = int(input("Enter your voice choice (1 or 2): ")) - 1
        if 0 <= choice < len(voices):
            engine.setProperty('Voice', voices[choice].id)
        else:
            print("Invalid choice. Defaulting to first voice.")
    else:
        engine.setProperty('Voice', voices[0].id)

# Function for Alexa to speak
def engine_talk(text):
    print(f"Alexa: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to capture user commands with error handling
def user_commands():
    # Get the number of available microphone devices
    num_devices = len(sr.Microphone.list_microphone_names())
    
    try:
        # Try different device indices from 0 to number of available devices
        for device_index in range(num_devices):
            with sr.Microphone(device_index=device_index) as source:
                print(f"Start Speaking! (Using device index: {device_index})")
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source)
                command = listener.recognize_google(voice).lower()
                if 'alexa' in command:
                    command = command.replace('alexa', '')
                print(f"User: {command}")
                return command
        # If none of the device indices work, return empty string
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio. Did you say something?")
        return ""
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service; {e}")
        return ""
# Main function for running Alexa
def run_alexa():
    command = user_commands()
    if command:
        if 'play' in command:
            song = command.replace('play', '')
            engine_talk(f"Playing {song}")
            try:
                pywhatkit.playonyt(song)
            except pywhatkit.exceptions.PyWhatKitException as e:
                print(f"Error playing video: {e}")
                engine_talk("Couldn't play the video.")
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            engine_talk('The current time is ' + time)
        elif 'who is' in command:
            name = command.replace('who is', '')
            info = wikipedia.summary(name, sentences=2)  # Get 2 sentences
            print(info)
            engine_talk(info)
        elif 'joke' in command:
            engine_talk(pyjokes.get_joke())
        elif 'stop' in command:
            sys.exit()
        else:
            engine_talk("I didn't catch that. Please speak again.")
    else:
        engine_talk("I didn't hear you properly.")

# Run Alexa in a loop
while True:
    # Choose voice (optional)
    # choose_voice()  # Uncomment to enable voice selection
    run_alexa()