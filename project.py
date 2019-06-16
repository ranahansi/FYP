import nltk

# Text Tokenization
fileObj = open('D:/Level 4 Semester 1/project/FYP/dataset/1.txt', 'r', encoding="mbcs")
text = fileObj.read()
tokens = nltk.sent_tokenize(text)
print(tokens)
