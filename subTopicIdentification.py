import maninTopicIdentification


def sub_topic_identification():
    text ="Tense relates to the time expressed by the verb. There are three main tenses. Past, for things that have already happened; present, for things that are happening right now; and future, for things that have not yet taken place. Each of these three tenses can be furthermodified by four aspects."
    sentences = maninTopicIdentification.sentence_tokenizer(text)

    # identifying the topic sentence.
    first_sentence = sentences[0]
    sub_topic__sentence = first_sentence
    print(sub_topic__sentence)

    # extracting key phrases with their frequencies.
    result1 = maninTopicIdentification.score_keyphrases_by_tfidf(text)
    result2 = maninTopicIdentification.score_keyphrases_by_textrank(text)
    print(result2)

    # extract the topic phrase from topic sentence.
    common_phrases_list = []
    for result in result2:
        key_phrase = result[0]
        similar_word_roots = maninTopicIdentification.check_root_of_word(key_phrase, sub_topic__sentence)
        similar_words = maninTopicIdentification.check_similarity(key_phrase, sub_topic__sentence)

        # check whether key phrase is in topic sentence.
        if str(key_phrase) in str(sub_topic__sentence):
            common_phrases_list.append(key_phrase)

        # check whether topic sentence contain synonyms of the given key phrase.
        elif similar_word_roots:
            for similar_word_root in similar_word_roots:
                common_phrases_list.append(similar_word_root)

        # check whether topic sentence contain similar words of the given key phrase.
        elif similar_words:
            for similar_word in similar_words:
                common_phrases_list.append(similar_word)

    print(common_phrases_list)
    first_phrase = common_phrases_list[0]
    last_phrase = common_phrases_list[len(common_phrases_list) - 1]

    # extracting significant phrase from topic sentence.
    sub_topic_phrase = (str(sub_topic__sentence).split(first_phrase))[1].split(last_phrase)[0]
    sub_topic = first_phrase + sub_topic_phrase + last_phrase

    if len(sub_topic) < 15:
        sub_topic_phrase = (str(sub_topic__sentence).split(last_phrase))[1].split(first_phrase)[0]
        sub_topic = last_phrase + sub_topic_phrase + first_phrase

#     check whether topic contain any not suitable punctuation marks.
    # define not suitable punctuation.
    punctuations = '''!()-[]{};:<>./?@#$%^&*_~'''

    has_punctuation = False
    for char in sub_topic:
        if char in punctuations:
            has_punctuation = True
            index_of_punctuation = sub_topic.index(char)
            break

    if has_punctuation:
        punctuation_mark = sub_topic[index_of_punctuation]
        extract_the_sub_topic = sub_topic.split(punctuation_mark)
        print(extract_the_sub_topic[0])
        sub_topic_of_the_content = extract_the_sub_topic[0]
    else:
        print(sub_topic)
        sub_topic_of_the_content = sub_topic

    print(sub_topic_of_the_content)


if __name__ == "__main__":
    sub_topic_identification()

