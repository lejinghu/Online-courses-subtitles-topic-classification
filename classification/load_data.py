import numpy as np

np.random.seed(1337)

import os

import sys

from keras.preprocessing import sequence

from keras.models import Sequential

from keras.layers import Dense

from keras.layers import Embedding

from keras.layers import GlobalAveragePooling1D

from keras.preprocessing.sequence import pad_sequences

from keras.utils.np_utils import to_categorical

import random

def load_test_data(TEXT_DATA_DIR):

    texts = []

    labels_index = {}

    labels = []

    for name in sorted(os.listdir(TEXT_DATA_DIR)):

        path = os.path.join(TEXT_DATA_DIR, name)

        if os.path.isdir(path):

            label_id = len(labels_index)

            labels_index[name] = label_id

            for fname in sorted(os.listdir(path)):
                title=(fname.split('_')[1])

                if(True):

                    fpath = os.path.join(path, fname)

                    if sys.version_info < (3,):

                        f = open(fpath)

                    else:

                        f = open(fpath, encoding='utf-8')

                    texts.append(f.read()+title)

                    f.close()

                    labels.append(label_id)



    print('Found %s test texts.' % len(texts))

    all_word=[]

    texts_cut=[]

    for t in texts:

        seg_list=list(t)

        all_word.extend(seg_list)

        texts_cut.extend([seg_list])



    return (texts_cut, labels)
