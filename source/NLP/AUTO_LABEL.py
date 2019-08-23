#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import json
import re

def auto_label(dataset,dictionary):
    '''
    인풋으로 '비속어사전'(dictionary)과 '필터링할 DataFrame'을 사용합니다.
     
    그러면 이 함수는 해당 dataFrame과 비속어사전을 매핑하여, 
    비속어사전에 있는 단어가 해당파일에 있는 경우에
    필터링된 파일(dataset)에 유해함 여부를 1로써 나타냅니다.
    
    이때 유해도를 나타내는 컬럼은 dataset에서 새로운 'filtered'에 나타나며
    filtered는 디폴트로 0 값을 갖고 있다가, 비속어 사전과 채팅의 데이터가 매핑되면
    유해도가 1로 변경됩니다.
      
    '''
# 1. 데이터 셋 불러오기
    datasets = dataset
        
# 2. 비속어 사전 불러오기
    with open(dictionary,'r') as f:
        forbiddenword = json.load(f)
        list2=list(forbiddenword.values()) 
        dict=list2[0] 
        dict1="|".join(dict) 
        
        
# 3. filtered라는 컬럼을 데이터셋에 추가함. (디폴트0, 필터되어 유해하면 1로 변경)
    datasets['filtered']=0
    data = datasets.comment

# 4. 유해 여부 실질적으로 판단
    idx = [i for i,d in enumerate(data) if re.search(dict1, d)]   
    datasets.iloc[idx,-1] = 1
    return datasets
#     return datasets[datasets['filtered']==1]
#=>필터된거만 보고싶을때
