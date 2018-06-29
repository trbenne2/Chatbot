'''
    This file is used to update and train the bot based on
    the word2vec.bin and the JSON file in the corpus best
    to use this file with a GPU because it is a lot and takes
    a lot of processing power
'''
import pickle
import numpy as np
from keras.models import Sequential, load_model
import gensim
from keras.layers.recurrent import LSTM, SimpleRNN
from sklearn.model_selection import train_test_split
import theano

theano.config.optimizer = "None"

with open('conversation.pickle') as f:
    vec_x, vec_y = pickle.load(open('conversation.pickle'))

vec_x = np.array(vec_x, dtype=np.float64)
vec_y = np.array(vec_y, dtype=np.float64)

# to test our accuracy
x_train, x_test, y_train, y_test = train_test_split(vec_x, vec_y, test_size=0.2, random_state=1)


'''
    implementation of LSTM 4 layers
    output dimension of 300 because it is length of the word    i.e. each word if 300
    input shape will be 15x300 because that's 1 sentence
    return true because we need 15 output dim
    initilization is glorot_normal???????????????????????/
    inner initilization is glorot_normal??????????????
    activation function is sigmoid
'''
model = Sequential()

model.add(LSTM(kernel_initializer="glorot_normal",
               input_shape=x_train.shape[1:],
               recurrent_initializer="glorot_normal",
               units=300,
               return_sequences=True,
               activation="sigmoid"))
model.add(LSTM(kernel_initializer="glorot_normal",
               input_shape=x_train.shape[1:],
               recurrent_initializer="glorot_normal",
               units=300,
               return_sequences=True,
               activation="sigmoid"))
model.add(LSTM(kernel_initializer="glorot_normal",
               input_shape=x_train.shape[1:],
               recurrent_initializer="glorot_normal",
               units=300,
               return_sequences=True,
               activation="sigmoid"))
model.add(LSTM(kernel_initializer="glorot_normal",
               input_shape=x_train.shape[1:],
               recurrent_initializer="glorot_normal",
               units=300,
               return_sequences=True,
               activation="sigmoid"))

'''
    loss is cosine_proximity because word2vec uses cosine prox as model of similarity between 2 words
    or distance between 2 words which measures error well
'''
model.compile(loss='cosine_proximity', optimizer='adam', metrics=['accuracy'])

'''
    fit in steps of 500
    save the models
'''

model = load_model('LSTM5000.h5')

model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM500.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM1000.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM1500.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM2000.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM2500.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM3000.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM3500.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM4000.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM4500.h5')
model.fit(x_train, y_train, nb_epoch=500, validation_data=(x_test, y_test))
model.save('LSTM5000.h5')
predictions = model.predict(x_test)
# mod = gensim.models(x_test)                                #right now this doesnt work need to look more into it
mod = gensim.models.Word2Vec.load('word2vec.bin')
[mod.most_similar([predictions[10][i]])[0] for i in range(15)]
