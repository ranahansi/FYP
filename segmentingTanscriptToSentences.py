import nltk

fileObj = open('data-sets/2.Principles and Words-20190603T102214Z-001/2.Principles and Words/1.txt', 'r', encoding="utf-8")
text = fileObj.read()
tokens = nltk.sent_tokenize(text)
splitText = text.splitlines()
print(splitText)
