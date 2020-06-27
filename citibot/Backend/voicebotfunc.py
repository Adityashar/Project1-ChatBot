import requests
import speech_recognition as sr     # import the library
import subprocess
from gtts import gTTS


def talk():

	message = ""
	bot_message = ""
	r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        
        r.adjust_for_ambient_noise(source)
        print("Speak Anything :")
        audio = r.listen(source, timeout=5)  # listen to the source
        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            print("You said : {}".format(message))

        except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
    if len(message)==0:
        continue

    for i, s in enumerate(message):
        if i < len(message)-1 and message[i] == ' ' and message[i-1].isdigit() and message[i+1].isdigit():
            message = message[:i] + message[i+1:]
    print("Sending message now...")

    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})

    print("Bot says, ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{bot_message}")

    return message, bot_message