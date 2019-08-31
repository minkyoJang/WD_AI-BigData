#!/usr/bin/env python
# coding: utf-8

# # utf-8로 인코딩시 단자음은  
# (227,132,177)부터 맨끝자리가 1오르면서(ex)(227,132,178)) 191까지가 ㄱ->ㄲ->ㄳ->ㄴ->ㄵ->ㄶ->ㄷ->ㄸ->ㄹ->ㄺ->ㄻ->ㄼ->ㄽ->ㄾ->ㄿ
# (227,133,128)부터 맨끝자리가 1오르면서 ㅎ은 (227 133 142) ㅏ는 (227 133 143) 마지막인 ㅣ는 (227 133 163)이다.

# # utf-8로 인코딩시 가부터
# 가:234, 176, 128,각:234, 176, 129 갂:234, 176, 130 갛:234, 176, 155 개:234, 176, 156~~ 갿: 234, 176, 191 끝이고
# 걀:234, 177, 128 ~~ 걿:234, 177, 191
# 검:234, 178, 128~~ 겿: 234, 178, 191
# 곀:234, 179, 128~~ 곿:234, 179, 191
# 관:234, 180, 128~~ 꿿234, 191, 191 이런 패턴으로 간다
# 뀀:235, 128, 128~~ 뿿235, 191, 191
# 쀀:236,128,128 ~~ 쿿:236 191 191
# 퀀:237 128 128 ~~ 힣:237, 158, 163
# 한글 도메인은 첫번째 자리가 234~237 두번째 자리가 128~191 세번째 자리가 128~191이다

# ## 결론
# 1. 첫째자리를 제외하고 모든 자리는 191이 끝이다
# 2. 해당자리가 191이 넘어가면 그 직전 자리가 1오른다.
# 3. 해당자리는 191이 넘어가면 128로 된다
# 4. 따라서 이것이 순환되므로 규칙은 찾을 수 있을것이다 다만 해당 글자 한 자(ㄱ~ㅣ)를 1대1로 매핑 시킬수가 없다.

# # 가:234, 176, 128
# # 낗:235, 130, 151
# 가-낗 1176
# 
# 나:235, 130, 152
# 닣:235, 139, 163
# 나-닣 588
# 
# 130:40
# 131~138:64
# 139:36
# 
# --> ㄱ,ㄲ,ㄴ,ㄷ,ㄸ,ㄹ,ㅁ,ㅂ,ㅃ,ㅅ,ㅆ,ㅇ,ㅈ,ㅉ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ
# 588을 더하면 같아야한다

# In[71]:


from functools import reduce


# In[4]:


def str_to_lst(char):
    """
    ex)"abcde"->['a','b','c','d','e']
    """
    lstt = []
    [lstt.append(_) for _ in char]
    return lstt


# In[5]:


def str_to_sep_utf8lst(str):
    """
    ex)"abc"->[[b'\xea\xb0\x80'], [b'\xea\xb0\xb8'], [b'\xea\xb1\xb0'], [b'\xea\xb2\xa8']]
    """
    morped =[[_.encode('utf-8')] for _ in str_to_lst(str)]
    return [[x for x in _] for _ in morped]


# In[6]:


def str_to_utf8lst(str):
    """
    ex)"abc"->[b'\xea\xb0\x80', b'\xea\xb0\xb8', b'\xea\xb1\xb0', b'\xea\xb2\xa8']
    """
    morped =[_.encode('utf-8') for _ in str_to_lst(str)]
    return morped


# In[45]:


def str_to_sep_numlst(str,sum=False):
    """
    ex)"abc"->[[234, 176, 128], [234, 176, 184], [234, 177, 176], [234, 178, 168]]
    """
    morped =[[_.encode('utf-8'),_] for _ in str_to_lst(str)]
    if sum:
        return [sum_238([x for x in _[0]]) for _ in morped]
    else :
        return [[x for x in _[0]] for _ in morped]


# In[8]:


def str_to_numlst(str):
    """
    ex)"abc"->[234, 176, 128,234, 176, 184,234, 177, 176,234, 178, 168]
    """
    li=[]
    morped =[[_.encode('utf-8'),_] for _ in str_to_lst(str)]
    sep_num_lst =[[x for x in _[0]] for _ in morped]
    [li.extend(lst) for lst in sep_num_lst]
    return  li


# In[9]:


def num_to_char(lst):
    """
    ex) [111,222,333,444,555]->abcde
    """
    byt=b''
    ntoh = [byt.fromhex(t) for t in [_.split('x')[1] for _ in [hex(x) for x in lst]]]
    byt2=b''
    byt2 = byt2.join(ntoh)
    return byt2.decode()


# In[12]:


def lst_to_num(lst):
    """
    ['가','나']->[1,2,3,4,5,6]
    """
    return list(map(str_to_numlst,lst))


# In[47]:


def lst_to_sepsumnum(lst):
    """
    ['가','나']->[[1+2+3],[4+5+6]]
    """
    return [str_to_sep_numlst(x,True) for x in lst]


# In[123]:


def sum_238(a):
    try:
        temp =238*238*a[0]+238*a[1]+a[2]-12889781
        
    except IndexError:
        print("한글이 아닙니다 리스트에서 한글 아닌것을 지우세요")    
    return temp    


# In[116]:


def sum_238s(a):
    try:
        temp =str(238*238*a[0]+238*a[1]+a[2]-12889781)
        return temp
    except IndexError:
        print("한글이 아닙니다 리스트에서 한글 아닌것을 지우세요")
        raise
    return temp


# In[93]:


def findchar(x):
    """
    use this func when sum 3 nums to mapping one char
    input is sum and output is char
    """
    a=[1,1,1]
    temp = x+12889781
    a[2] = temp%238
    temp =int(temp/238)
    a[1] = temp%238
    a[0] =int(temp/238)
    return num_to_char(a)


# In[107]:


def sepnum_to_char(lst):
    """
    input is 2d list and out put is string
    """
    temp = [[findchar(x) for x in lst[i]]  for i in range(len(lst))]
    res = [[reduce(lambda x,y: x+y,temp[i])] for i in range(len(temp))]
    return res

