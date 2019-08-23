import numpy as np
import pandas as pd
from konlpy.tag import Okt
import tensorflow as tf
from tensorflow.python.keras.preprocessing import sequence
from tensorflow import keras
import pickle
import warnings



def run_model(uploaded_txt):
    warnings.filterwarnings(action='ignore')
    print(uploaded_txt)
    morp = Okt()
    print(morped = morp.morphs(uploaded_txt, norm=True, stem=True))
    # print(morped)

    
    # load vocab
    with open('./NLP/vocab/vocab_index.pickle', 'rb') as f:
        vocab_index = pickle.load(f)
    with open('./NLP/vocab/vocab_inverted_index.pickle', 'rb') as f:
        vocab_inverted_index = pickle.load(f)

    def text_to_index(tokens):
        oov_id = 1
        indexes = []
        for tok in tokens:
            if tok in vocab_index:
                indexes.append(vocab_index[tok])
            else:
                indexes.append(oov_id)

        return indexes


    pad_id = 0

    x_variable = [text_to_index(morped)]
    
    sentence_size = 20
    x_padded = sequence.pad_sequences(x_variable,
                                     maxlen=sentence_size,
                                     truncating='post',
                                     padding='post',
                                     value=pad_id)
    # print(x_padded)
    # Load model
    new_model = keras.models.load_model('./model/cnn_oversample.h5')

    # predict
    predict_prob = new_model.predict(x_padded)
    print(predict_prob)
    return predict_prob[0][1]