import datetime
import numpy as np
import gensim
import nltk
from keras.models import load_model
import theano

from smarthome import smarthome_commands

import server

theano.config.optimizer = "None"

model = load_model('LSTM5000.h5')  # import the last saved model
mod = gensim.models.Word2Vec.load('word2vec.bin')  # and word2vec
# file path to log the user text to update the JSON for training
log_path = "dialog_from_user.txt"
log_file = open(log_path, 'a')
tday = datetime.datetime.today().strftime(
    "<<<<<<<<<<%B %d, %Y: %H:%M:%S>>>>>>>>>>")
log_file.write(tday + "\n")


# todo: so rachana said just work on the conversation json and get that to work with commands and for use to come up
# todo: things to put in the conversation.json

def predict_from_bot(message):

    #     # if there is a command
    #     if 'lights' in message:
    #         smartHomeDevice('lights')     #check to see if the device is connected
    #     elif 'temperature' in message or 'thermostat' in message:
    #         smartHomeDevice('thermostat')
    # #todo: need to make function reconize commands

    log_file.write(message + "\n")
    # lightbulb(message)                  # Smart home device
    sentend = np.ones((300L,), dtype=np.float32)  # python V2 add L behind 3

    sent = nltk.word_tokenize(message.lower())  # tokenize the message
    sentvec = [mod[w]
               for w in sent if w in mod.vocab]  # find the word to vector


    sentvec[14:] = []
    sentvec.append(sentend)
    if len(sentvec) < 15:
        for i in range(15 - len(sentvec)):
            sentvec.append(sentend)
    sentvec = np.array([sentvec])

    predictions = model.predict(sentvec)  # predict based on input
    # find word most similar in word vec
    outputlist = [mod.most_similar([predictions[0][i]])[
        0][0] for i in range(15)]

    for x in range(len(outputlist)):  # get rid of the extra from the vector
        if outputlist[x].__contains__("kleiser") \
                or outputlist[x].__contains__("karluah") \
                or outputlist[x].__contains__("ballets"):
            outputlist[x] = ""

    output = str(' '.join(outputlist))
    output.rstrip()

    # print type(output)

    # send to smarthome.py and determine command
    command = smarthome_commands(output)

    return command


def testing_no_server():
    x = raw_input("Enter the message:")  # get message
    command = predict_from_bot(x)
    print command['message']
    print command

def server_running():
    server.run()
    pass


def main():
    while (True):
        # testing_no_server()
        server_running()


if __name__ == '__main__':
    main()

