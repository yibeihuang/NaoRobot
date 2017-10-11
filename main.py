import json
from EmotionAPI import get_emotion
from say_contents import say_contents, get_sentence
from videoInput_getImage import showNaoImage


def main(IP, PORT):
	emotion = None
	while emotion==None:
		showNaoImage(IP, PORT)
		path = 'camImage.png'
		emotion = get_emotion(path)
	sentence = get_sentence(emotion)
	say_contents(sentence, IP, PORT)


if __name__ == "__main__":
    with open('config.json') as f:
    	data = json.load(f)
    IP = data.get("IP").encode("utf-8")
    PORT = data.get("PORT")
    main(IP, PORT)