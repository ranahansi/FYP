# Python 2.x program to transcribe an Audio file
import os
import nltk
import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


fileObj = open('data-sets/2.Principles and Words-20190603T102214Z-001/2.Principles and Words/1.txt', 'r', encoding="utf-8")
text = fileObj.read()
tokens = nltk.sent_tokenize(text)
splitText = text.splitlines()
print(splitText)
AUDIO_FILE = ("audio set/0.31.wav")

# use the audio file as the audio source

r = sr.Recognizer()

with sr.AudioFile(AUDIO_FILE) as source:
    # reads the audio file. Here we use record instead of
    # listen
    audio = r.record(source)

try:
    audio_content = r.recognize_google(audio)
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(audio_content)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            search_word = w
            for u in splitText:
                if search_word in u:
                    filtered_sentence.append(u)
                    break
                else:
                    print("The word is not in the text")
                print(type(filtered_sentence))
    print("The last element of list using reverse : "+ str(filtered_sentence[0]))

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")

except sr.RequestError as e:
    print("Could not request results from Google SpeechRecognitionservice;{0}".format(e))
