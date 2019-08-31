from konlpy.tag import Okt
from tqdm import tqdm
import pickle
from tensorflow.python.keras.preprocessing import sequence
import os


def index_to_text(indexes, vocab_inverted_index):
    return ' '.join([vocab_inverted_index[i] for i in indexes])

def text_to_index(tokens, vocab_index):
    oov_id=1
    indexes = []
    for tok in tokens:
        if tok in vocab_index:
            indexes.append(vocab_index[tok])
        else:
            indexes.append(oov_id)

    return indexes

def chat_to_morp(chat):
    '''
    채팅을 형태소 분석 후
    단어사전 불러와 워드벡터로 변환 후
    패딩하여 반환합니다.
    param chat : Series or list of chat
    return : padded sequence
    '''
    morp = Okt()
    morped = [morp.morphs(_, norm=True, stem=True) for _ in tqdm(chat)]

    # load vocab
    with open(os.getcwd()+'/vocab/vocab_index.pickle', 'rb') as f:
        vocab_index = pickle.load(f)
    with open(os.getcwd()+'/vocab/vocab_inverted_index.pickle', 'rb') as f:
        vocab_inverted_index = pickle.load(f)

    pad_id = 0


    x_variable = [text_to_index(_, vocab_index) for _ in morped]

    sentence_size = 10
    x_padded = sequence.pad_sequences(x_variable,
                                    maxlen=sentence_size,
                                    value=pad_id)

    return x_padded
