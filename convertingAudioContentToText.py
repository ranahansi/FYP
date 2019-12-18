import difflib
import nltk
import speech_recognition as spreg
from nltk.corpus import stopwords
import convertVideoToAudio
import maninTopicIdentification


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
    delimiter = ".\n"
    sentence_tokens_items = text.split(delimiter)
    sentence_tokens = []
    for sentence_token_item in sentence_tokens_items:
        sentence = sentence_token_item.replace("\n", "")
        sentence_tokens.append(sentence)
    return sentence_tokens


# transcribe the audio file.
def transcribe_audio_file(file_path):
    """transcribe the audio file"""
    sound_file = file_path
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
        except spreg.RequestError as e:
            print("Request error from Google Speech Recognition service; {}".format(e))


# method to segmenting transcribe text by the time
def segmenting_transcribe_text(audio_list):
    """method to segmenting transcribe text by the time"""
    transcribe_text_list = []
    transcribe_key = 1
    for audio in audio_list:
        transcribe_text_dic = {}
        audio_file_path = audio.get('file path')
        audio_file_time = audio.get('time')
        transcribe_text_dic['key'] = transcribe_key
        transcribe_text_dic['time'] = audio_file_time
        transcribe_text = transcribe_audio_file(audio_file_path)
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
    stop_words = set(stopwords.words('english'))
    filtered_text_tokens = []

    for w in text_tokens:
        if w not in stop_words:
            filtered_text_tokens.append(w)
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
            d = seq.ratio() * 100
            if d > 75:
                similar_words.append(token2)
                break
    return similar_words


# method to identify time based relevant content
def content_identifier(sentence_tokens, text_tokens):
    """method to identify time based relevant content"""
    selected_sentences = []
    for sentence_token in sentence_tokens:
        sentence_token_str = word_tokenizing(str(sentence_token))
        convert_to_lower_case = map(str.lower, sentence_token_str)
        lower_case_sentence_token_list = list(convert_to_lower_case)
        after_checking_similarity_words = check_similarity(lower_case_sentence_token_list, text_tokens)
        total_word_count = len(lower_case_sentence_token_list)
        similar_words = set(lower_case_sentence_token_list) & set(text_tokens)
        similar_words_list = list(similar_words)
        total_similar_words = after_checking_similarity_words + similar_words_list
        word_count = len(total_similar_words)
        total_word_count_percentage = (word_count * total_word_count)/100

        if word_count >= 5:
            selected_sentences.append(sentence_token)
        else:
            break
    return selected_sentences


# main method to segmenting transcript content according to audio segments
def audio_transcript_segmentation(audio_list, main_audio_transcript):
    """control the main method"""
    text_document_content = read_the_transcript_file(main_audio_transcript)
    sentence_token_content = sentence_tokenizer(text_document_content)
    transcribe_text_list = segmenting_transcribe_text(audio_list)
    time_align_contents = []
    for transcribe_text in transcribe_text_list:
        sentence_tokens = sentence_token_content
        time_align_content = {}
        key = transcribe_text.get('key')
        time = transcribe_text.get('time')
        text = transcribe_text.get('transcribe text')
        if text != 0:
            text_tokens = word_tokenizing(str(text))
            filtered_text_tokens = stop_words_remover(text_tokens)
            lower_case__filtered_text_token_map = map(str.lower, filtered_text_tokens)
            lower_case__filtered_text_token_list = list(lower_case__filtered_text_token_map)
            print(lower_case__filtered_text_token_list)
            time_align_content['key'] = key
            time_align_content['time'] = time
            time_align_content_list = []
            time_align_content['sentences'] = time_align_content_list
            list_indexes = []
            for sentence_token in sentence_tokens:
                print(sentence_token)
                sentence_token_str = word_tokenizing(str(sentence_token))
                sentence_token_without_stop_words = stop_words_remover(sentence_token_str)
                lower_case_text_token_map = map(str.lower, sentence_token_without_stop_words)
                lower_case_text_token_list = list(lower_case_text_token_map)
                print(lower_case_text_token_list)
                similar_words_list = set(lower_case__filtered_text_token_list) & set(lower_case_text_token_list)
                sorted_similar_words_last_according_to_transcribe_text = sorted(similar_words_list, key=lambda k: lower_case__filtered_text_token_list.index(k))
                similar_words_list_first = list(sorted_similar_words_last_according_to_transcribe_text)
                print(similar_words_list_first)
                length_of_the_transcribe_text = len(lower_case__filtered_text_token_list)
                if len(similar_words_list_first) > (length_of_the_transcribe_text/2):
                    index_of_sentence = sentence_tokens.index(sentence_token)
                    list_indexes.append(index_of_sentence)
                    time_align_content_list.append(sentence_token)
                    del sentence_tokens[:index_of_sentence+1]
                    break

                elif len(similar_words_list_first) >= 4 and len(similar_words_list_first) <= (length_of_the_transcribe_text/2):
                    index_of_sentence = sentence_tokens.index(sentence_token)
                    list_indexes.append(index_of_sentence)
                    time_align_content_list.append(sentence_token)

                else:
                    if list_indexes:
                        index_of_sentence = sentence_tokens.index(sentence_token)
                        list_indexes.append(index_of_sentence)
                        length_of_indexes_list = len(list_indexes)
                        considered_value = list_indexes[length_of_indexes_list-1]
                        considered_index = list_indexes.index(considered_value)
                        del sentence_tokens[:considered_index]
                        break
                    else:
                        continue

            time_align_contents.append(time_align_content)

    text_file_1 = open('output.txt', 'w')
    for time_align_content in time_align_contents:
        text_file_1.write('-----------------------------------\n')
        text_file_1.write(str(time_align_content.get('key'))+'\n')
        text_file_1.write('-----------------------------------\n')
        text_file_1.write(str(time_align_content.get('time'))+'\n')
        text_file_1.write('-----------------------------------\n')
        text_file_1.write(str(time_align_content.get('sentences')[:]))

    text_file_1.close()

    return time_align_contents
