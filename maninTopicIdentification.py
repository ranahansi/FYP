import difflib
from itertools import takewhile, tee
import itertools

import networkx
import nltk
import string
import gensim
import spacy
from nltk.stem import PorterStemmer

porter_stemmer = PorterStemmer()


def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    """this method for extracting chunks"""
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                    for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase
    candidates = [' '.join(word for word, pos, chunk in group).lower()
                  for key, group in itertools.groupby(all_chunks, lambda word__pos__chunk: word__pos__chunk != 'O') if key]

    return [cand for cand in candidates
            if cand not in stop_words and not all(char in punct for char in cand)]


def extract_candidate_words(text, good_tags=set(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])):
    """this method for extracting words"""
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize and POS-tag words
    tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent)
                                                                    for sent in nltk.sent_tokenize(text)))
    # filter on certain POS tags and lowercase all words
    candidates = [word.lower() for word, tag in tagged_words
                  if tag in good_tags and word.lower() not in stop_words
                  and not all(char in punct for char in word)]

    return candidates


def score_keyphrases_by_tfidf(texts, candidates='chunks'):
    """this method is used for get the tfidf of key-phrases"""
    # extract candidates from each text in texts, either chunks or words
    if candidates == 'chunks':
        boc_texts = [extract_candidate_chunks(text) for text in texts]
    elif candidates == 'words':
        boc_texts = [extract_candidate_words(text) for text in texts]
    # make gensim dictionary and corpus
    dictionary = gensim.corpora.Dictionary(boc_texts)
    corpus = [dictionary.doc2bow(boc_text) for boc_text in boc_texts]
    # transform corpus with tf*idf model
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    return corpus_tfidf, dictionary


def score_keyphrases_by_textrank(text, n_keywords=0.05):
    """this method is used for get the text rank of key-phrases"""
    # tokenize for all words, and extract *candidate* words
    words = [word.lower()
             for sent in nltk.sent_tokenize(text)
             for word in nltk.word_tokenize(sent)]
    candidates = extract_candidate_words(text)
    # build graph, each node is a unique candidate
    graph = networkx.Graph()
    graph.add_nodes_from(set(candidates))

    # iterate over word-pairs, add unweighted edges into graph
    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a_from_pair, b_from_pair = tee(iterable)
        next(b_from_pair, None)
        return zip(a_from_pair, b_from_pair)

    for word1, word2 in pairwise(candidates):
        if word2:
            graph.add_edge(*sorted([word1, word2]))
    # score nodes using default pagerank algorithm, sort by score, keep top n_keywords
    ranks = networkx.pagerank(graph)
    if 0 < n_keywords < 1:
        n_keywords = int(round(len(candidates) * n_keywords))
    word_ranks = {word_rank[0]: word_rank[1]
                  for word_rank in sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:n_keywords]}
    keywords = set(word_ranks.keys())
    # merge keywords into keyphrases
    keyphrases = {}
    j = 0
    for i, word in enumerate(words):
        if i < j:
            continue
        if word in keywords:
            kp_words = list(takewhile(lambda x: x in keywords, words[i:i + 10]))
            avg_pagerank = sum(word_ranks[w] for w in kp_words) / float(len(kp_words))
            keyphrases[' '.join(kp_words)] = avg_pagerank
            # counter as hackish way to ensure merged keyphrases are non-overlapping
            j = i + len(kp_words)

    return sorted(keyphrases.items(), key=lambda x: x[1], reverse=True)


# method for sentence tokenizer in transcript.
def sentence_tokenizer(text):
    """method for sentence tokenizer in transcript"""
    nlp = spacy.load('en_core_web_sm')
    # generating sentences list.
    about_doc = nlp(text)
    sentence_tokens = list(about_doc.sents)
    len(sentence_tokens)
    return sentence_tokens


# method to word tokenizer
def word_tokenizing(text):
    """method to word tokenizer"""
    word_tokens = nltk.word_tokenize(str(text))
    return word_tokens


# check the word that has same root like given word
def check_root_of_word(key_phrase, main_topic__sentence):
    """check whether given word has synonyms in given main topic sentence"""
    similar_root_words = []
    tokenized_main_topic_sentence = word_tokenizing(main_topic__sentence)
    main_topic_tokens_without_punctuation = removing_punctuation(tokenized_main_topic_sentence)
    tokenized_key_phrase = word_tokenizing(key_phrase)
    tokenized_key_phrase_without_punctuation = removing_punctuation(tokenized_key_phrase)
    if len(tokenized_key_phrase_without_punctuation) == 1:
        for token in main_topic_tokens_without_punctuation:
            topic_sentence_word_root = porter_stemmer.stem(str(token))
            key_phrase_word_root = porter_stemmer.stem(tokenized_key_phrase_without_punctuation[0])
            if topic_sentence_word_root == key_phrase_word_root:
                similar_root_words.append(key_phrase_word_root)
                break
    return similar_root_words


# check the similarity of two words.
def check_similarity(key_phrase, main_topic__sentence):
    """check whether given two words are similar or not"""
    similar_words = []
    tokenized_main_topic_sentence = word_tokenizing(main_topic__sentence)
    main_topic_tokens_without_punctuation = removing_punctuation(tokenized_main_topic_sentence)
    for token in main_topic_tokens_without_punctuation:
        seq = difflib.SequenceMatcher(None, token, key_phrase)
        similarity = seq.ratio() * 100
        if similarity > 75:
            similar_words.append(token)
            break
    return similar_words


# remove punctuation marks in given list.
def removing_punctuation(tokens):
    """this method is used for removing punctuations"""
    punctuations = '''!()-[]{};:'",<>./?@#$%^&*_~'''
    for token in tokens:
        if token in punctuations:
            tokens.remove(str(token))
    return tokens


def write_sentence_tokens_to_text_file(sentence_tokens_to_topics_identification):
    """This method is used to write tokenized sentences to text file for topic identification"""
    output_text_file = open("myOutFile.txt", "w", encoding='utf-8')
    for line in sentence_tokens_to_topics_identification:
        # write line to output file
        output_text_file.write(str(line))
        output_text_file.write("\n")
    output_text_file.close()


# method to read the transcript file.
def read_the_transcript_file(file_path):
    """method to read the transcript file"""
    # open and read the transcript file.
    file_obj = open(file_path, 'r', encoding="cp1252")
    # removing unnecessary spaces.
    text = file_obj.read().replace("\n", "")
    return text


def main_topic_identification(main_audio_transcript):
    """main method to generate time-aligned content"""
    text = read_the_transcript_file(main_audio_transcript)
    sentence_tokens = sentence_tokenizer(text)
    sentence_tokens_to_topics_identification = sentence_tokens
    write_sentence_tokens_to_text_file(sentence_tokens_to_topics_identification)
    # read the sentence tokenized transcript file.
    file_obj = open('myOutFile.txt', 'r', encoding="utf8")
    text = file_obj.read()
    sentences = sentence_tokenizer(text)

    # identifying the topic sentence.
    first_sentence = sentences[0]
    second_sentence = sentences[1]
    third_sentence = sentences[2]
    if len(first_sentence) > 15:
        main_topic__sentence = first_sentence
    elif len(second_sentence) > 15:
        first_sentence = second_sentence
        main_topic__sentence = first_sentence
    else:
        first_sentence = third_sentence
        main_topic__sentence = first_sentence

    # extracting key phrases with their frequencies.
    result2 = score_keyphrases_by_textrank(text)

    # print score of keyphrases by tfidf.
    # new_topics = result1[0]
    # for topic in new_topics:
    #     print(topic)

    # extract the topic phrase from topic sentence.
    common_phrases_list = []
    for result in result2:
        key_phrase = result[0]
        similar_word_roots = check_root_of_word(key_phrase, main_topic__sentence)
        similar_words = check_similarity(key_phrase, main_topic__sentence)

        # check whether key phrase is in topic sentence.
        if str(key_phrase) in str(main_topic__sentence):
            common_phrases_list.append(key_phrase)

        # check whether topic sentence contain synonyms of the given key phrase.
        elif similar_word_roots:
            for similar_word_root in similar_word_roots:
                common_phrases_list.append(similar_word_root)

    #     check whether topic sentence contain similar words of the given key phrase.
        elif similar_words:
            for similar_word in similar_words:
                common_phrases_list.append(similar_word)
    first_phrase = common_phrases_list[0]
    last_phrase = common_phrases_list[len(common_phrases_list)-1]

    # extracting significant phrase from topic sentence.
    main_topic_phrase = (str(main_topic__sentence).split(first_phrase))[1].split(last_phrase)[0]
    main_topic = first_phrase + main_topic_phrase + last_phrase

    if len(main_topic) < 15:
        main_topic_phrase = (str(main_topic__sentence).split(last_phrase))[1].split(first_phrase)[0]
        main_topic = last_phrase + main_topic_phrase + first_phrase

#     check whether topic contain any not suitable punctuation marks.
    # define not suitable punctuation.
    punctuations = '''!()-[]{};:<>./?@#$%^&*_~'''

    has_punctuation = False
    for char in main_topic:
        if char in punctuations:
            has_punctuation = True
            index_of_punctuation = main_topic.index(char)
            break
    if has_punctuation:
        punctuation_mark = main_topic[index_of_punctuation]
        extract_the_main_topic = main_topic.split(punctuation_mark)
        main_topic_of_the_transcript = extract_the_main_topic[0]
    else:
        main_topic_of_the_transcript = main_topic

    # writing the topic sentence inside the text file.
    file = open("output text files/verb tenses and verb moods.txt", "a")
    print(main_topic_of_the_transcript, file=file)
    file.close()

    return main_topic_of_the_transcript


def compare_two_main_topics(video_main_topic, transcript_main_topic):
    """this method is used to compare two topics comming under the video and transcript"""
    # Calculate your similarity value
    similar_word_set = set(transcript_main_topic) and set(video_main_topic)
    if similar_word_set:
        return video_main_topic
