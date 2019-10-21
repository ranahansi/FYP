import re
import nltk
import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import convertVideoToAudio


def audioTranscriptSegmentation():
    fileObj = open('data-sets/2.Principles and Words-20190603T102214Z-001/2.Principles and Words/1.txt', 'r', encoding="utf-8")
    text = fileObj.read()
    tokens = nltk.sent_tokenize(text)
    splitText = text.splitlines()
    audioFileList = convertVideoToAudio.audioSegmentation()
    new_dict = {}
    for audio_filepath in audioFileList:

        r = sr.Recognizer()

        with sr.AudioFile(audio_filepath) as source:
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

            if not filtered_sentence:
                key_of_dict = re.findall("\d+\.\d+", audio_filepath)
                new_dict[key_of_dict[0]] = "No content available"
                break
            else:
                print("The last element of list using reverse : " + str(filtered_sentence[0]))
                updatedIndex = splitText.index(str(filtered_sentence[0])) + 1
                text_content_name = splitText[:updatedIndex]
                key_of_dict = re.findall("\d+\.\d+", audio_filepath)
                new_dict[key_of_dict[0]] = text_content_name
                del splitText[:updatedIndex]
                print(splitText)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google SpeechRecognitionservice;{0}".format(e))
    new_dict["remaining"] = splitText
    print(new_dict)

    return new_dict
