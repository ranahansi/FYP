import nltk
from nltk.corpus import stopwords

# Text tokenization.
fileObj = open('D:/Level 4 Semester 1/project/FYP/dataset/1.txt', 'r', encoding="mbcs")
text = fileObj.read()
words = nltk.word_tokenize(text)

# Identifying stops words in english.
stopWords = set(stopwords.words('english'))
wordsFiltered = []

# Filtering stopwords.
for w in words:
    if w not in stopWords:
        wordsFiltered.append(w)

# Chunking words in equal word count
# n = no.of words
n = 10
final = [wordsFiltered[i * n:(i + 1) * n] for i in range((len(wordsFiltered) + n - 1) // n)]

with open('output.txt', 'w') as f:
    for item in final:
        f.write("%s\n" % item)
