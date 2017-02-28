#! /usr/bin/python3.6
# coding: utf-8

from keras.datasets import imdb
import numpy as np
from matplotlib import pyplot as plt
from keras.models import Sequential

from keras.layers import Dense, Activation

start_index=3
vocab_size=10000 # or None for everything
(X_train, y_train), (X_test, y_test) = imdb.load_data(path="imdb_full.pkl",
                                                      nb_words=vocab_size,
                                                      skip_top=0,
                                                      maxlen=None,
                                                      seed=113,
                                                      start_char=1,
                                                      oov_char=3,
                                                      index_from=start_index)

def sent2binaryVector (sentence):
    v = np.zeros([vocab_size])
    for i in range(1,len(sentence)):
        v[sentence[i]-start_index]=1
    return v



def convertCorpus2binary(corpus):
    M = np.zeros([len(corpus),vocab_size])
    i=0
    for x in corpus:
        v = sent2binaryVector(x)
        M[i,:] = v
        i+=1
    return M

train = convertCorpus2binary(X_train)
test = convertCorpus2binary(X_test)

print(len(train), " ", train.shape)
print(type(train[0]), " ", train[0].shape)



model = Sequential()
model.add(Dense(output_dim=1, input_dim=vocab_size))
model.add(Activation('sigmoid'))


model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()



history = model.fit(train, y_train,
        nb_epoch=10,
        batch_size=128,
        validation_data=(test, y_test))

print(type(history))
print(history.params)
print(history.epoch)
print(history.history["acc"])


x = history.epoch
y = history.history["acc"]
y_prime = history.history['val_acc']

plt.plot(x,y)
plt.plot(x,y_prime)
plt.show()
