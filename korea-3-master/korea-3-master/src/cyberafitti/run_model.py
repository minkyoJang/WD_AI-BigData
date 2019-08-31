from utils.bp_processing import bp_tokenize
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import torch
from attention.attention_model import StructuredSelfAttention
from torch.autograd import Variable
import os
import pickle
from utils.visualize_attention import *


class RunAttentionModel(object):
    

    

    def __init__(self, input_text):
        '''
        input_text : 1-d sequence of String, Series 가능
        '''

        # model parameter 
        self._MAX_LEN = 50
        self._VOCAB_SIZE = 260
        self._EMB_DIM = 10

        self.input_text = input_text
        # model load
        self.model = torch.load(os.getcwd()+'/model/self_attention_bp_mixed_10.pt')
        
    def predict(self):
        # bpe preprocessing
        self.tokenized = bp_tokenize(self.input_text)
        # padding preprocessing
        self.input_padded = pad_sequences(self.tokenized, maxlen=self._MAX_LEN)
        # batch size initial
        self.model.batch_size = np.array(self.input_padded).shape[0]
        # hidden state initial
        self.model.hidden_state = self.model.init_hidden()
        input_tensor = Variable(torch.from_numpy(self.input_padded).type(torch.LongTensor))

        self.pred, self.attwts = self.model(input_tensor)
        
        return

    def run_demo(self):
        '''
        데모 실행 시 호출
        return : 1-d numpy array, 유해정도 probabilyty
        '''

        return self.pred.data.numpy()


    def run_bj(self):
        '''
        return : float, bj 유해 비율 
        '''
        bj_count = torch.round(self.pred.type(torch.DoubleTensor).squeeze(1)).sum().data.numpy()
        
        return bj_count / len(self.input_text)

    def visualize(self):
        '''
        어텐션 시각화 함수
        return : (String type) javaScript
        '''
        
        # 텍스트를 어텐션 모델 인풋 길이와 똑같게끔 만들어준다.
        chat_to_bytelength = chat_to_byteLength(self.input_text[0])[-50:]
        chat_to_bytelength = '_'*(50-len(chat_to_bytelength)) + chat_to_bytelength
        print(len(chat_to_bytelength))
        # 어텐션 차원을 합한다.
        wts_add = torch.sum(self.attwts, 1).data.numpy()[0]

        
        return createJS(chat_to_bytelength, wts_add)




if __name__ == '__main__':
    import run_model
    from attention.attention_model import StructuredSelfAttention
    tmp = run_model.RunAttentionModel(['ㅋ'])

    tmp.predict()
    print(tmp.visualize())

    # print(tmp.run_bj())


    # print(tmp.run_demo())

