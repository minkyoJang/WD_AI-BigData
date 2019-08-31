#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
import tensorflow as tf
from tensorflow.python.keras.preprocessing import sequence
from tensorflow import keras
from tqdm import tqdm
from collections import Counter
from matplotlib import pyplot as plt
import pickle
from utils import morp_preprocessing


# In[2]:


import re
from konlpy.tag import Okt
okt = Okt()

def prep1(textt = '존ㄴ ㅂ신 병ㅅ 새ㄲ ㅈ나 ㅅ발 ㅁㅊ놈아'):
    pattern2 = re.compile(r'[^ 5a-zA-Zㄱ-ㅊㅌ-ㅠㅢ가-힣]')
    textt = pattern2.sub('',textt)
    temp_okt = okt.pos(textt) # , norm=True, stem=True
    
    cut_word_h = []
    cut_word_e = []
    temp = []
    
    for a in range(len(temp_okt)):
        if temp_okt[a][1] == 'Alpha':
            cut_word_e.append(temp_okt[a])
        else:
            cut_word_h.append(temp_okt[a])
    
    cut_word_h.extend(cut_word_e)
    temp.extend(cut_word_h)
    
    temp2 = []
    string1 = ''
    k = -1

    # 병신, 시발, 씨발, 존나, 느금마, 씨발롬들아, 미친놈아, 새끼, 좆밥
    bad_word = ['ㅂ', 'ㅅ', 'ㅆ', 'ㅈ', 'ㅁㅊ', 'ㄲ', 'ㄴ']
    bad_set_word = ['신', '발', '빨', '나', '놈', '끼', '밥', '문대', '대로', '망겜']
    important_class = ['KoreanParticle', 'Noun', 'mixed', 'Verb', 'Adjective', 'Alpha']
    not_important_word = ['은', '는', '이', '가', '자']

    for i in range(len(temp)):
        if temp[i][0] in bad_word:
            if i < len(temp) - 1 and len(temp) > 1 and temp[i+1][0] in bad_set_word:
                if temp[i+1][1] == 'Noun' and temp[i+1][0] not in not_important_word:
                    for j in range(i):
                        if j <= k or temp[j][1] not in important_class or (len(temp[j][0]) > 6 and temp[j][1] == 'Verb') or temp[j][0] in not_important_word:
                            continue
                        temp2.append(temp[j])
                    string1 = temp[i][0] + temp[i+1][0]
                    temp2.append((string1, 'mixed'))
                    k = i+1
            else:
                if i != 0 and len(temp[i-1][0]) == 1 and  temp[i-1][1] == 'Noun' and temp[i-1][0] not in not_important_word:
                    for j in range(i):
                        if j <= k or temp[j][1] not in important_class or (len(temp[j][0]) > 6 and temp[j][1] == 'Verb') or temp[j][0] in not_important_word:
                            continue
                        temp2.append(temp[j])
                    string1 = temp[i-1][0] + temp[i][0]
                    temp2.pop()
                    temp2.append((string1, 'mixed'))
                    k = i

        if i < len(temp) - 1 and len(temp) > 1:
            if temp[i][1] == 'Noun' and temp[i+1][1] == 'Suffix' and temp[i+1][0] not in not_important_word:
                for j in range(i):
                    if j <= k or temp[j][1] not in important_class or (len(temp[j][0]) > 6 and temp[j][1] == 'Verb') or temp[j][0] in not_important_word:
                        continue
                    temp2.append(temp[j])
                string1 = temp[i][0] + temp[i+1][0]
                temp2.append((string1, 'Noun + Suffix'))
                k = i+1
                
        # 형태소분석기가 인식못하는 예외단어
        if i < len(temp) - 1 and len(temp) > 1:
            if (temp[i][0] == '운' and temp[i+1][0] == '지') or (temp[i][0] == '노' and temp[i+1][0] == '무현')            or (temp[i][0] == '찐' and temp[i+1][0] == '따') or (temp[i][0] == '섹' and temp[i+1][0] == '히')            or (temp[i][0] == '새' and temp[i+1][0] == '키') or (temp[i][0] == '새' and temp[i+1][0] == '퀴')            or (temp[i][0] == '도' and temp[i+1][0] == '네') or (temp[i][0] == '장애' and temp[i+1][0] == '인색히')            or (temp[i][0] == '자' and temp[i+1][0] == '지') or (temp[i][0] == '고' and temp[i+1][0] == '소')            or (temp[i][0] == '저능' and temp[i+1][0] == '아') or (temp[i][0] == '색' and temp[i+1][0] == '히')            or (temp[i][0] == '쓰래' and temp[i+1][0] == '기') or (temp[i][0] == '애' and temp[i+1][0] == '미')            or (temp[i][0] == 'ㅅ' and temp[i+1][0] == 'ㅂ') or (temp[i][0] == 'ㅂ' and temp[i+1][0] == 'ㅅ')            or (temp[i][0] == 'ㅈ' and temp[i+1][0] == 'ㄹ') or (temp[i][0] == 'ㅈ' and temp[i+1][0] == 'ㄴ')            or (temp[i][0] == 'ㅁ' and temp[i+1][0] == 'ㅊ') or (temp[i][0] == 'ㅅ' and temp[i+1][0] == 'ㄲ')            or (temp[i][0] == 'ㅈ' and temp[i+1][0] == 'ㅂ') or (temp[i][0] == '섯' and temp[i+1][0] == '네')            or (temp[i][0] == '섰' and temp[i+1][0] == '네') or (temp[i][0] == '섯' and temp[i+1][0] == '다')            or (temp[i][0] == '섰' and temp[i+1][0] == '다') or (temp[i][0] == '시' and temp[i+1][0] == '발')            or (temp[i][0] == '새' and temp[i+1][0] == '끼') or (temp[i][0] == '개간' and temp[i+1][0] == '년')            or (temp[i][0] == '시부' and temp[i+1][0] == '렬') or (temp[i][0] == '쳐' and temp[i+1][0] == '받는')            or (temp[i][0] == '닝' and temp[i+1][0] == '기리') or (temp[i][0] == '개' and temp[i+1][0] == '공감')            or (temp[i][0] == '개' and temp[i+1][0] == '새기') or (temp[i][0] == '빠' and temp[i+1][0] == '가')            or (temp[i][0] == '개' and temp[i+1][0] == '소리') or (temp[i][0] == '개' and temp[i+1][0] == '쉽다')            or (temp[i][0] == '개' and temp[i+1][0] == '쉽네') or (temp[i][0] == '개' and temp[i+1][0] == '싫다')            or (temp[i][0] == '계' and temp[i+1][0] == '새끼') or (temp[i][0] == '김치' and temp[i+1][0] == '녀')            or (temp[i][0] == '에' and temp[i+1][0] == '라이') or (temp[i][0] == '관' and temp[i+1][0] == '종')            or (temp[i][0] == '괘' and temp[i+1][0] == '새끼') or (temp[i][0] == '그' and temp[i+1][0] == '켬')            or (temp[i][0] == '꼬' and temp[i+1][0] == '라지') or (temp[i][0] == '노' and temp[i+1][0] == '알라')            or (temp[i][0] == '노친' and temp[i+1][0] == '네') or (temp[i][0] == '눈' and temp[i+1][0] == '깔')            or (temp[i][0] == '니' and temp[i+1][0] == '년') or (temp[i][0] == '이' and temp[i+1][0] == '년')            or (temp[i][0] == '머' and temp[i+1][0] == '갈') or (temp[i][0] == '덜' and temp[i+1][0] == '떨어진')            or (temp[i][0] == '시' and temp[i+1][0] == '바알') or (temp[i][0] == '또' and temp[i+1][0] == '라인')            or (temp[i][0] == '시' and temp[i+1][0] == '펄') or (temp[i][0] == '디' and temp[i+1][0] == '쥐고싶냐')            or (temp[i][0] == '병' and temp[i+1][0] == '신') or (temp[i][0] == '존' and temp[i+1][0] == '나')            or (temp[i][0] == '섹' and temp[i+1][0] == '스') or (temp[i][0] == '니' and temp[i+1][0] == '미')            or (temp[i][0] == '미' and temp[i+1][0] == '친') or (temp[i][0] == '느' and temp[i+1][0] == '그')            or (temp[i][0] == '어' and temp[i+1][0] == '미') or (temp[i][0] == '느' and temp[i+1][0] == '금')            or (temp[i][0] == '메' and temp[i+1][0] == '갈') or (temp[i][0] == '일' and temp[i+1][0] == '베')            or (temp[i][0] == '병' and temp[i+1][0] == '자') or (temp[i][0] == '장' and temp[i+1][0] == '애')            or (temp[i][0] == '씨' and temp[i+1][0] == '발') or (temp[i][0] == '븽' and temp[i+1][0] == '신')            or (temp[i][0] == '빨' and temp[i+1][0] == '아') or (temp[i][0] == '새' and temp[i+1][0] == '낀데')            or (temp[i][0] == '개' and temp[i+1][0] == '같이') or (temp[i][0] == '슴' and temp[i+1][0] == '가')            or (temp[i][0] == '정신병' and temp[i+1][0] == '자') or (temp[i][0] == '친구' and temp[i+1][0] == '년')            or (temp[i][0] == '오' and temp[i+1][0] == '지구') or (temp[i][0] == '오' and temp[i+1][0] == '쪘')            or (temp[i][0] == '5' and temp[i+1][0] == '졌') or (temp[i][0] == '5' and temp[i+1][0] == '지구')            or (temp[i][0] == '5' and temp[i+1][0] == '지네') or (temp[i][0] == '5' and temp[i+1][0] == '지고')            or (temp[i][0] == '머리' and temp[i+1][0] == '텅') or (temp[i][0] == '쪼' and temp[i+1][0] == '다')            or (temp[i][0] == '디' and temp[i+1][0] == '질') or (temp[i][0] == '뒤' and temp[i+1][0] == '질')            or (temp[i][0] == '디' and temp[i+1][0] == '졌') or (temp[i][0] == '딴' and temp[i+1][0] == '년')            or (temp[i][0] == '또' and temp[i+1][0] == '라이') or (temp[i][0] == '똘' and temp[i+1][0] == '아이')            or (temp[i][0] == '오' and temp[i+1][0] == '쪘') or (temp[i][0] == '명존' and temp[i+1][0] == '쎄')            or (temp[i][0] == '미시' and temp[i+1][0] == '친발') or (temp[i][0] == '주' and temp[i+1][0] == '겨')            or (temp[i][0] == '윾' and temp[i+1][0] == '두') or (temp[i][0] == '기' and temp[i+1][0] == '무띠')            or (temp[i][0] == '죽여뿌' and temp[i+1][0] == '고') or (temp[i][0] == '미' and temp[i+1][0] == '틴')            or (temp[i][0] == '별' and temp[i+1][0] == '창') or (temp[i][0] == '색' and temp[i+1][0] == '희')            or (temp[i][0] == '수준' and temp[i+1][0] == '하고는') or (temp[i][0] == '쉬이' and temp[i+1][0] == '바')            or (temp[i][0] == '시미' and temp[i+1][0] == '발친') or (temp[i][0] == '시미' and temp[i+1][0] == '친발')            or (temp[i][0] == '시' and temp[i+1][0] == '부울') or (temp[i][0] == '시방' and temp[i+1][0] == '새')            or (temp[i][0] == '시불' and temp[i+1][0] == '탱') or (temp[i][0] == '시' and temp[i+1][0] == '빨')            or (temp[i][0] == '시' and temp[i+1][0] == '이발') or (temp[i][0] == '개시' and temp[i+1][0] == '키')            or (temp[i][0] == '시' and temp[i+1][0] == '팔') or (temp[i][0] == '십' and temp[i+1][0] == '창')            or (temp[i][0] == '쓰' and temp[i+1][0] == '렉') or (temp[i][0] == '씨' and temp[i+1][0] == '바라')            or (temp[i][0] == '씨방' and temp[i+1][0] == '새') or (temp[i][0] == '개' and temp[i+1][0] == '년')            or (temp[i][0] == '개' and temp[i+1][0] == '같네') or (temp[i][0] == '개' and temp[i+1][0] == '같아')            or (temp[i][0] == '개' and temp[i+1][0] == '같다') or (temp[i][0] == '처' and temp[i+1][0] == '먹어')            or (temp[i][0] == '처' and temp[i+1][0] == '먹다') or (temp[i][0] == '처' and temp[i+1][0] == '먹여')            or (temp[i][0] == '씨' and temp[i+1][0] == '이발') or (temp[i][0] == '씨' and temp[i+1][0] == '바알')            or (temp[i][0] == '졀' and temp[i+1][0] == '라') or (temp[i][0] == '졌' and temp[i+1][0] == '같은')            or (temp[i][0] == '조' and temp[i+1][0] == '낸') or (temp[i][0] == '족' and temp[i+1][0] == '까')            or (temp[i][0] == '존' and temp[i+1][0] == '쎄') or (temp[i][0] == '좁' and temp[i+1][0] == '밥')            or (temp[i][0] == '종' and temp[i+1][0] == '나') or (temp[i][0] == '싸' and temp[i+1][0] == '물어')            or (temp[i][0] == '닭' and temp[i+1][0] == '쳐') or (temp[i][0] == '닦' and temp[i+1][0] == '쳐')            or (temp[i][0] == '닭' and temp[i+1][0] == '근혜') or (temp[i][0] == '쥐박' and temp[i+1][0] == '이')            or (temp[i][0] == '죵' and temp[i+1][0] == '나') or (temp[i][0] == '줬' and temp[i+1][0] == '같은')            or (temp[i][0] == '쥰' and temp[i+1][0] == '나') or (temp[i][0] == '쥰' and temp[i+1][0] == '니')            or (temp[i][0] == '지' and temp[i+1][0] == '롤') or (temp[i][0] == '와' and temp[i+1][0] == '꾸')            or (temp[i][0] == '짱' and temp[i+1][0] == '께') or (temp[i][0] == '존' and temp[i+1][0] == '맛')            or (temp[i][0] == '쳐' and temp[i+1][0] == '먹어') or (temp[i][0] == '쳐' and temp[i+1][0] == '먹다')            or (temp[i][0] == '쳐' and temp[i+1][0] == '발라') or (temp[i][0] == '쳐' and temp[i+1][0] == '바르다')            or (temp[i][0] == '개' and temp[i+1][0] == '사기') or (temp[i][0] == '오지' and temp[i+1][0] == '네')            or (temp[i][0] == '지' and temp[i+1][0] == '린다') or (temp[i][0] == '지리' and temp[i+1][0] == '네')            or (temp[i][0] == '십' and temp[i+1][0] == '가능') or (temp[i][0] == '빡' and temp[i+1][0] == '고수')            or (temp[i][0] == '라인' and temp[i+1][0] == '빨') or (temp[i][0] == '개' and temp[i+1][0] == '무시')            or (temp[i][0] == '뇨' and temp[i+1][0] == '속') or (temp[i][0] == '찌리' and temp[i+1][0] == '네')            or (temp[i][0] == '시' and temp[i+1][0] == '부레')            :
                for j in range(i):
                    if j <= k or temp[j][1] not in important_class or (len(temp[j][0]) > 6 and temp[j][1] == 'Verb') or temp[j][0] in not_important_word:
                        continue
                    temp2.append(temp[j])
                string1 = temp[i][0] + temp[i+1][0]
                temp2.append((string1, 'Except'))
                k = i+1
                
        # 형태소분석기가 인식못하는 예외단어(3글자)
        if i < len(temp) - 2 and len(temp) > 2:
            if (temp[i][0] == '앙' and temp[i+1][0] == '기' and temp[i+2][0] == '무')            or (temp[i][0] == '앙' and temp[i+1][0] == '기' and temp[i+2][0] == '무띠')            or (temp[i][0] == '보' and temp[i+1][0] == '딩고' and temp[i+2][0] == '지')            or (temp[i][0] == '앙' and temp[i+1][0] == '기모' and temp[i+2][0] == '띄')            or (temp[i][0] == '시' and temp[i+1][0] == '새' and temp[i+2][0] == '발끼')            or (temp[i][0] == '씨' and temp[i+1][0] == '새' and temp[i+2][0] == '발끼')            or (temp[i][0] == '시' and temp[i+1][0] == '친' and temp[i+2][0] == '발미')            or (temp[i][0] == '죠' and temp[i+1][0] == '온' and temp[i+2][0] == '나')            or (temp[i][0] == '에' and temp[i+1][0] == '반' and temp[i+2][0] == '데')            or (temp[i][0] == '개' and temp[i+1][0] == '웃' and temp[i+2][0] == '기네')            :
                for j in range(i):
                    if j <= k or temp[j][1] not in important_class or (len(temp[j][0]) > 6 and temp[j][1] == 'Verb') or temp[j][0] in not_important_word:
                        continue
                    temp2.append(temp[j])
                string1 = temp[i][0] + temp[i+1][0] + temp[i+2][0]
                temp2.append((string1, 'Except'))
                k = i+2
        
        # 형태소분석기가 인식못하는 예외단어(4글자)
        if i < len(temp) - 3 and len(temp) > 3:
            if (temp[i][0] == '앙' and temp[i+1][0] == '기' and temp[i+2][0] == '모' and temp[i+3][0] == '띠')            or (temp[i][0] == '앙' and temp[i+1][0] == '기' and temp[i+2][0] == '모' and temp[i+3][0] == '딱')            :
                for j in range(i):
                    if j <= k or temp[j][1] not in important_class or (len(temp[j][0]) > 6 and temp[j][1] == 'Verb') or temp[j][0] in not_important_word:
                        continue
                    temp2.append(temp[j])
                string1 = temp[i][0] + temp[i+1][0] + temp[i+2][0] + temp[i+3][0]
                temp2.append((string1, 'Except'))
                k = i+3
        
        # 예외단어(엿)
        if temp[i][0] == '엿'and temp[i][1] == 'Modifier':
            for j in range(i):
                if j <= k or temp[j][1] not in important_class or (len(temp[j][0]) > 6 and temp[j][1] == 'Verb') or temp[j][0] in not_important_word:
                    continue
                temp2.append(temp[j])
            string1 = temp[i][0]
            temp2.append((string1, 'Except'))
            k = i
            
    else:
        for j in range(len(temp)):
            if j <= k or temp[j][1] not in important_class or (len(temp[j][0]) > 6 and temp[j][1] == 'Verb') or temp[j][0] in not_important_word:
                continue
            temp2.append(temp[j])

    result = []
    
    for b in range(len(temp2)):
        result.append(temp2[b][0])
    
    return result


# In[3]:


def prep2(X, y):
    '''
    comments, label 을 넣어주세요
    '''
    listy = list(y)
    chat = list()
    for i,x in tqdm(enumerate(X)):
        temp = []
        temp.append(prep1(x))
        if temp == [[]]:
            del listy[i]
            continue
        else:
            chat.extend(temp)
    
    return chat, listy


# In[ ]:




