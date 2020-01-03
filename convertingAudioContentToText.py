import string
import nltk
import difflib
import speech_recognition as spreg
from nltk.corpus import stopwords
import maninTopicIdentification
import re
import convertVideoToAudio


# method to read the transcript file.
def read_the_transcript_file(file_path):
    """method to read the transcript file"""
    # open and read the transcript file.
    file_obj = open(file_path, 'r')
    # removing unnecessary spaces.
    text = file_obj.read()
    return text


# method for sentence tokenizer in transcript.
def sentence_tokenizer(text):
    """method for sentence tokenizer in transcript"""
    # delimiters = ".\n", "?", "!", ":\n", "."
    # regex_pattern = '|'.join(map(re.escape, delimiters))
    # sentence_tokens_list = re.split(regex_pattern, text)
    sentence_tokens_list = re.split(r'(?<=[\.\n|\?])\s*', text)
    sentence_tokens = []
    for sentence in sentence_tokens_list:
        sentence = sentence.replace("\n", " ")
        sentence_tokens.append(sentence)
        print(sentence)
    return sentence_tokens


# transcribe the audio file.
def transcribe_audio_file(file_path, audio_file_duration, audio_file_time):
    """transcribe the audio file"""
    sound_file = file_path
    if audio_file_duration < 40:
        recog = spreg.Recognizer()
        with spreg.AudioFile(sound_file) as source:
            # use record instead of listning
            speech = recog.record(source)
            try:
                text = recog.recognize_google(speech, language="en-AUS")
                # print('The file contains: ' + text)
                return text
            except spreg.UnknownValueError:
                # print('Unable to recognize the audio')
                return 0
            except spreg.RequestError as exeption:
                print("Request error from Google Speech Recognition service; {}".format(exeption))
    else:
        text = transcribe_large_audio(sound_file, audio_file_duration, audio_file_time)
        return text


# method to transcribe large audio file.
def transcribe_large_audio(sound_file, audio_file_duration, audio_file_time):
    time_sub_list = []
    time_sub_list.append(audio_file_duration/2)
    time_sub_list.append(audio_file_duration)
    audio_sub_list = convertVideoToAudio.sub_audio_segmentation(time_sub_list, sound_file, audio_file_time)
    text_content = " "
    for audio in audio_sub_list:
        recog = spreg.Recognizer()
        with spreg.AudioFile(audio) as source:
            # use record instead of listning
            speech = recog.record(source)
            try:
                text = recog.recognize_google(speech, language="en-AUS")
                text_content = text_content + text
                # print('The file contains: ' + text)
            except spreg.UnknownValueError:
                # print('Unable to recognize the audio')
                return 0
            except spreg.RequestError as exeption:
                print("Request error from Google Speech Recognition service; {}".format(exeption))
    return text_content


# method to segmenting transcribe text by the time
def segmenting_transcribe_text(audio_list):
    """method to segmenting transcribe text by the time"""
    transcribe_text_list = []
    transcribe_key = 1
    for audio in audio_list:
        transcribe_text_dic = {}
        audio_file_path = audio.get('file path')
        audio_file_time = audio.get('time')
        audio_file_duration = audio.get('duration')
        transcribe_text_dic['key'] = transcribe_key
        transcribe_text_dic['time'] = audio_file_time
        transcribe_text = transcribe_audio_file(audio_file_path, audio_file_duration, audio_file_time)
        if transcribe_text != 0:
            transcribe_text_dic['transcribe text'] = transcribe_text
        else:
            transcribe_text_dic['transcribe text'] = 0
        transcribe_text_list.append(transcribe_text_dic)
        transcribe_key = transcribe_key + 1
    return transcribe_text_list


# method to word tokenizer
def word_tokenizing(text):
    """method to word tokenizer"""
    word_tokens = nltk.word_tokenize(text)
    return word_tokens


# method to remove stop words
def stop_words_remover(text_tokens):
    """method to remove stop words"""
    punctuations = str(string.punctuation)
    stop_words = str(stopwords.words('english')) + str(punctuations)
    filtered_text_tokens = []

    for word in text_tokens:
        if word not in stop_words:
            filtered_text_tokens.append(word)
    return filtered_text_tokens


# method to check given word in sentence
def check_word_in_sentence(word, sentence):
    """method to check given word in sentence"""
    if word in sentence:
        return True


# check the similarity of two words.
def check_similarity(sentence_token_str, text_tokens):
    """check whether given two words are similar or not"""
    similar_words = []
    sentence_token_str_without_punctuation = maninTopicIdentification.removing_punctuation(sentence_token_str)
    for token1 in text_tokens:
        for token2 in sentence_token_str_without_punctuation:
            seq = difflib.SequenceMatcher(None, token1, token2)
            similarity = seq.ratio() * 100
            if similarity > 75:
                similar_words.append(token2)
                break
    return similar_words


# method to identify time based relevant content
def content_identifier(sentence_token, filtered_text_tokens):
    """method to identify time based relevant content"""
    sentence_token_str = word_tokenizing(str(sentence_token))
    lower_case_text_token_map = map(str.lower, sentence_token_str)
    lower_case_text_token_list = list(lower_case_text_token_map)
    sentence_token_without_stop_words = stop_words_remover(lower_case_text_token_list)
    sentence_token_without_punctuations = removing_punctuation(sentence_token_without_stop_words)
    print(sentence_token_without_punctuations)
    mostly_similarly_words_list = set(
        check_similarity(filtered_text_tokens, sentence_token_without_punctuations))
    similar_words_list = set(filtered_text_tokens) & set(sentence_token_without_punctuations)
    all_similar_word_list = mostly_similarly_words_list.union(similar_words_list)
    sorted_similar_words_last_according_to_transcribe_text = sorted(all_similar_word_list, key=lambda
        k: filtered_text_tokens.index(k))
    print(sorted_similar_words_last_according_to_transcribe_text)
    return sorted_similar_words_last_according_to_transcribe_text, len(sentence_token_without_punctuations)


# remove punctuation marks in given list.
def removing_punctuation(tokens):
    """method to removing punctuation marks"""
    punctuations = '''!()-[]{};:'",,<>./?@#$%^&*_~'''
    for token in tokens:
        if token in punctuations:
            tokens.remove(str(token))
    return tokens


# main method to segmenting transcript content according to audio segments
def audio_transcript_segmentation(audio_list, main_audio_transcript):
    """control the main method"""
    # method call
    text_document_content = read_the_transcript_file(main_audio_transcript)
    # method call
    sentence_token_content = sentence_tokenizer(text_document_content)
    print(sentence_token_content)
    # method call
    transcribe_text_list = segmenting_transcribe_text(audio_list)
    print(transcribe_text_list)
    time_align_contents = []
    # get the each transcribe text and analyzing.
    for transcribe_text in transcribe_text_list:
        sentence_tokens = sentence_token_content
        # creating dictionary items and getting value from transcribe text list.
        time_align_content = {}
        key = transcribe_text.get('key')
        time = transcribe_text.get('time')
        text = transcribe_text.get('transcribe text')
        if text != 0:
            # manupulating text in transcribe text.
            text_tokens = word_tokenizing(str(text))
            lower_case__filtered_text_token_map = map(str.lower, text_tokens)
            lower_case__filtered_text_token_list = list(lower_case__filtered_text_token_map)
            filtered_text_tokens = stop_words_remover(lower_case__filtered_text_token_list)
            print(filtered_text_tokens)
            length_of_transcribe_text = len(filtered_text_tokens)
            time_align_content['key'] = key
            time_align_content['time'] = time
            time_align_content_list = []
            time_align_content['sentences'] = time_align_content_list
            list_indexes = []
            for sentence_token in sentence_tokens:
                # manupulating text in sentence.
                print(sentence_token)
                sorted_similar_words_last_according_to_transcribe_text, length_of_the_sentence = content_identifier(sentence_token, filtered_text_tokens)
                similar_words_list_first = list(sorted_similar_words_last_according_to_transcribe_text)
                print(similar_words_list_first)
                # length_of_transcribe_text = len(lower_case__filtered_text_token_list)
                # checking data and append to the final list.
                if len(similar_words_list_first) >= (int(length_of_the_sentence / 2)):
                    index_of_sentence = sentence_tokens.index(sentence_token)
                    list_indexes.append(index_of_sentence)
                    time_align_content_list.append(sentence_token)

                else:
                    if len(list_indexes) >= 2:
                        index_of_sentence = sentence_tokens.index(sentence_token)
                        list_indexes.append(index_of_sentence)
                        length_of_indexes_list = len(list_indexes)
                        considered_value = list_indexes[length_of_indexes_list-1]
                        considered_index = list_indexes.index(considered_value)
                        del sentence_tokens[:considered_index]
                        break
                    else:
                        index_of_sentence = sentence_tokens.index(sentence_token)
                        list_indexes.append(index_of_sentence)
                        time_align_content_list.append(sentence_token)
                        continue

            time_align_contents.append(time_align_content)

    # if there any remaining sentences of transcript.It also append to the list.
    if sentence_tokens:
        for sentence_token in sentence_tokens:
            length_of_the_final_list = len(time_align_contents)
            acess_last_dict_of_list = time_align_contents[length_of_the_final_list-1]
            last_dic_time_align_content = acess_last_dict_of_list.get('sentences')
            last_dic_time_align_content.append(sentence_token)

    # write the output in text file.
    text_file_1 = open('output.txt', 'w')
    for time_align_content in time_align_contents:
        text_file_1.write('-----------------------------------\n\n')
        text_file_1.write(str(time_align_content.get('key'))+'\n')
        text_file_1.write('-----------------------------------\n\n')
        text_file_1.write(str(time_align_content.get('time'))+'\n')
        text_file_1.write('-----------------------------------\n\n')
        sentences = time_align_content.get('sentences')
        for sentence in sentences:
            text_file_1.write(str(sentence)+'\n')

    text_file_1.close()

    return time_align_contents
