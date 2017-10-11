# -*- encoding: UTF-8 -*-
from naoqi import ALProxy
import codecs
import json

def say_from_string(tts, strname):
    to_say = strname.encode("utf-8")
    tts.say(to_say)

def say_contents(strname, IP, PORT):
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    tts.setLanguage('English')
    # encodings
    say_from_string(tts, strname)

def get_sentence(emotion):
    NAME = 'Yibei'
    if emotion=='happiness':
        sentence = "Hello {}, you look {} today".format(NAME,'happy')
    elif emotion=='sadness':
        sentence = "Hello {}, why do you look so {} today".format(NAME,'sad')
    elif emotion=='anger':
        sentence = "Hello {}, why do you look so {} today".format(NAME,'angry')
    elif emotion=='fear':
        sentence = "Hello {}, anything {} today?".format(NAME,'scary')
    elif emotion=='surprise':
        sentence = "Hello {}, why do you look so {} today".format(NAME,'suprised')
    else:
        sentence = "Hello {}, how are you today".format(NAME)
    return sentence

if __name__ == "__main__":
    with open('config.json') as f:
        data = json.load(f)
    IP = data.get("IP").encode("utf-8")
    PORT = data.get("PORT")
    say_contents('Test', IP, PORT)