import re
import nltk
import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import convertVideoToAudio

# method to segmenting transcript content according to audio segments
def audioTranscriptSegmentation():
    # open and read the transcript file.
    fileObj = open('data-sets/verb tences and verb moods.txt', 'r', encoding="utf-8")
    text = fileObj.read()

    # sentence tokenization in transcript.
    tokens = nltk.sent_tokenize(text)
    splitText = text.splitlines()

    # method call to segmenting audio file
    audioFilePathList = convertVideoToAudio.audioSegmentation()
    timestamp_sentences_content = {}
    for audio_filepath in audioFilePathList:

        r = sr.Recognizer()

        with sr.AudioFile(audio_filepath) as source:
            # reads the audio file. Here we use record instead of
            # listen
            audio = r.record(source)

        try:
            audio_content = r.recognize_google(audio, language='en')

            stop_words = set(stopwords.words('english'))

            #word tokenization
            word_tokens = word_tokenize(audio_content)

            filtered_sentence = []
            # Removing stop words from the transcribe content
            for w in word_tokens:
                if w not in stop_words:
                    search_word = w
                    for u in splitText:
                        if search_word in u:
                            # apending sentences to list which are first occurence in searched word.
                            filtered_sentence.append(u)
                            break

            if not filtered_sentence:
                key_of_dict = re.findall("\d+\.\d+", audio_filepath)
                timestamp_sentences_content[key_of_dict[0]] = "No content available"
                break
            else:
                print("The last element of list using reverse : " + str(filtered_sentence[0]))
                updatedIndex = splitText.index(str(filtered_sentence[0])) + 1
                text_content_name = splitText[:updatedIndex]

                # Extracting floating point(timestamp of frame change) from string
                key_of_dict = re.findall("\d+\.\d+", audio_filepath)
                timestamp_sentences_content[key_of_dict[0]] = text_content_name
                del splitText[:updatedIndex]

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google SpeechRecognitionservice;{0}".format(e))
    timestamp_sentences_content["remaining"] = splitText

    return timestamp_sentences_content
