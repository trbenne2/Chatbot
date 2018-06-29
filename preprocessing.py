#imports for preprocessing for the chatbot training
import os
import json
import nltk
#nltk.download()                #had to do this so line 38 would work need to get nltk tools
import gensim
import numpy as np
import pickle


os.getcwd()    #need this for the nltk to work
model = gensim.models.Word2Vec.load('word2vec.bin')     #pretrained from apnews Skip-gram corpos
path2 = "corpus"
file = open(path2+ '/conversation.json')        #data to edit the bot for training and more
data = json.load(file)                          #load the json file
cor = data["conversations"]                 #put the json into a dictionary ["conversation"]

x = []
y = []

print(len(cor))
'''
    append questions and answers
'''
for i in range(len(cor)):
    for j in range(len(cor[i])):
        if j<len(cor[i]) - 1:
            x.append(cor[i][j])
            y.append(cor[i][j+1])


'''
    Tokenize questions and answers
'''
token_x = []
token_y = []
for i in range(len(x)):
    token_x.append(nltk.tokenize.word_tokenize(x[i].lower()))
    token_y.append(nltk.tokenize.word_tokenize(y[i].lower()))

'''
    Create vector of all ones so can append at end of sentence
    
'''
sentend = np.ones((300,),dtype=np.float32)                  #add L behind 300 in Python V2


'''
    for every word in vocab/corpas we try to find the vector for it in or word2vec model
    creating a sentence to be word vector
'''
vec_x = []
for sent in token_x:
    sentvec = [model[w] for w in sent if w in model.vocab]
    vec_x.append(sentvec)

vec_y = []
for sent in token_y:
    sentvec = [model[w] for w in sent if w in model.vocab]
    vec_y.append(sentvec)


'''
    clipping off words in sentences with the the length of 15
'''
for token_sent in vec_x:
    token_sent[14:] = []
    token_sent.append(sentend)

for token_sent in vec_x:
    if len(token_sent)<15:
        for i in range(15-len(token_sent)):
            token_sent.append(sentend)

for token_sent in vec_y:
    token_sent[14:] = []
    token_sent.append(sentend)

for token_sent in vec_y:
    if len(token_sent) < 15:
        for i in range(15 - len(token_sent)):
            token_sent.append(sentend)

'''
    save as pickle dumb so we can directly put in the preprocessing into the model
    directly load model and use
'''
with open('conversation.pickle', 'wb') as f:                # Python V2 get rid of b in wb
    pickle.dump([vec_x, vec_y], f)