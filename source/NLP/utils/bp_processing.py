from tqdm import tqdm
import numpy as np


def bp_tokenize(chat):
    '''
    chat : sequence of chat (String)
    return : byte tokenized 2-dim array
    '''
    encoded = [_.encode('utf-8') for _ in tqdm(chat)]
    bytearr = np.array([list(map(str, _)) for _ in encoded])

    return bytearr

if __name__ == '__main__':
    print(bp_tokenize(['시발', 'ㅋㅋ', 'ㅅㅂ', 'ㅅ1ㅂ', 'ㅄ']))