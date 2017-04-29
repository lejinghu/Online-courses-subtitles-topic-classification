# encoding=utf-8
#from __future__ import print_function
import os
import numpy as np
import pandas as pd
np.random.seed(1337)
import random

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.layers import Dense, Input, Flatten, merge, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.layers import GlobalAveragePooling1D,GlobalMaxPooling1D
from keras.models import Model, Sequential
import load_data
import sys

TEXT_DATA_DIR = 'C text 5 28/'
MAX_SEQUENCE_LENGTH = 900
EMBEDDING_DIM = 300
NUM_OF_EPOCHS=6

print('Processing text dataset')

texts = []
labels_index = {}
labels = []
for name in sorted(os.listdir(TEXT_DATA_DIR)):
    path = os.path.join(TEXT_DATA_DIR, name)
    if os.path.isdir(path):
        label_id = len(labels_index)
        labels_index[name] = label_id
        for fname in sorted(os.listdir(path)):
            if(True):
                fpath = os.path.join(path, fname)
                if sys.version_info < (3,):
                    f = open(fpath)
                else:
                    f = open(fpath, encoding='utf-8')
                texts.append(f.read())
                f.close()
                labels.append(label_id)

print('Found %s texts.' % len(texts))

all_word=[]
texts_cut=[]
for t in texts:
    seg_list=list(t)
    all_word.extend(seg_list)
    texts_cut.extend([seg_list])

words= set(all_word)
word2idx = dict((v, i) for i, v in enumerate(words))
idx2word = list(words)

sentences_idx=[]
for single_text in texts_cut:
    single_idx=[]
    for single_word in single_text:
        single_idx.extend([word2idx[single_word]+1])
    sentences_idx.extend([single_idx])

x_train=sentences_idx
y_train = to_categorical(np.asarray(labels, dtype='int32'))

test_texts_cut,test_labels=load_data.load_test_data('srtcut/')
y_test=to_categorical(np.asarray(test_labels, dtype='int32'))
test_sentences_idx=[]
for test_single_text in test_texts_cut:
    test_single_idx=[]
    for test_single_word in test_single_text:
        test_single_idx.extend([word2idx.get(test_single_word,-1)+1])
    test_sentences_idx.extend([test_single_idx])

x_test=test_sentences_idx

print('Average train sequence length: {}'.format(np.mean(list(map(len, x_train)), dtype=int)))
print('Average test sequence length: {}'.format(np.mean(list(map(len, x_test)), dtype=int)))
MAX_SEQUENCE_LENGTH=int(np.mean(list(map(len, x_train))))+int(np.mean(list(map(len, x_test))))

x_train = pad_sequences(x_train, maxlen=MAX_SEQUENCE_LENGTH)
x_test = pad_sequences(x_test, maxlen=MAX_SEQUENCE_LENGTH)
print('Preparing embedding matrix.')


# Embedding
nb_words = len(words)+1
embedding_layer=Embedding(nb_words,
                    EMBEDDING_DIM,
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=True
                            )
print('Training model.')


# train a 1D convnet with global maxpooling
sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)
x1 = Conv1D(128, 1, activation='relu')(embedded_sequences)
x1 = GlobalMaxPooling1D()(x1)
x2 = Conv1D(128, 2, activation='relu')(embedded_sequences)
x2 = GlobalMaxPooling1D()(x2)
x3 = Conv1D(128, 3, activation='relu')(embedded_sequences)
x3 = GlobalMaxPooling1D()(x3)
x4 = Conv1D(128, 4, activation='relu')(embedded_sequences)
x4 = GlobalMaxPooling1D()(x4)
x5 = Conv1D(128, 5, activation='relu')(embedded_sequences)
x5 = GlobalMaxPooling1D()(x5)

x = merge([ x2, x3, x4, x5], mode='concat')

preds = Dense(len(labels_index), activation='softmax')(x)

model = Model(sequence_input, preds)
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])



model.fit(x_train,y_train, validation_data=(x_test, y_test),nb_epoch=NUM_OF_EPOCHS, batch_size=128)
proba=model.predict(x_test,verbose=1)
#print y_train
print (y_test)
print (proba)

ilen=len(proba)
jlen=len(proba[0])
probalist=[]
for y in range(0, jlen):
    probalist.append(0)

guesslist=[]
for y in range(0, jlen):
    guesslist.append(0)

for x in range(0, ilen):
    tempy=[]
    y= np.argmax(proba[x])
    tempy.append(y)
    if(ilen-x>1):
        ya= np.argmax(proba[x+1])
        tempy.append(ya)
    if(ilen-x>2):
        yb= np.argmax(proba[x+2])
        tempy.append(yb)
    
    if(x>1):
        y1= np.argmax(proba[x-1])
        tempy.append(y1)
    if(x>2):
        y2= np.argmax(proba[x-2])
        tempy.append(y2)

    y=max(set(tempy), key=tempy.count)
    guesslist[y]+=1#I guess it is
    if(y_test[x][y]==1):
        probalist[y]+=1# And I guess right
		
countlist=[]
for y in range(0, jlen):
    countlist.append(0)
for x in range(0, ilen):
    y= np.argmax(y_test[x])
    countlist[y]+=1

print ("I am right:")
print (probalist)
print ("I thought I was right:")
print (guesslist)
print ("This is actually right:")
print (countlist)

c = 0
p = 0
r = 0
n = jlen
for y in range(0, jlen):
    print (probalist[y]/(countlist[y]*1.0))
    c += probalist[y]
    r += probalist[y]/(countlist[y]*1.0)

for y in range(0, jlen):
    if(guesslist[y]==0):
        print (0)
    else:
        print (probalist[y]/(guesslist[y]*1.0))
        p += probalist[y]/(guesslist[y]*1.0)

print('c=%d, n=%d' % (c, ilen/jlen))
print('p=%f, r=%f, f=%f' % (p/n, r/n, 2.0*p*r/(p+r)/n))
#print c, p, r
#print c*1.0/p, c*1.0/r

#import time
#localtime= time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) 
#np.savetxt("recording/"+localtime+".csv", proba, delimiter=",")