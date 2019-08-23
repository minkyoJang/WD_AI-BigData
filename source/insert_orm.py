#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'watermark')
get_ipython().run_line_magic('watermark', '-a JaeEunPark -u -d -p sqlalchemy')


# In[1]:


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import Query, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
import requests


# In[55]:


engine = create_engine('sqlite:///cyberafitti.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()


# In[56]:


class Netloc(base):
    __tablename__ = 'Netloc'
    
    id = Column(Integer, primary_key=True)
    netloc = Column(String, nullable=False)
    
    
class Bj(base):
    __tablename__='Bj'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    blacklist = Column(Boolean, nullable=False, default=False)
    netloc_id = Column(Integer, ForeignKey('Netloc.id'), nullable=False)
    
    
class Url(base):
    __tablename__ = 'Url'
    
    id = Column(Integer, primary_key=True)
    netloc_id = Column(Integer, ForeignKey('Netloc.id'), nullable=False)
    path = Column(String, nullable=False)
    param = Column(String, nullable=True)
    bj_id = Column(Integer, ForeignKey('Bj.id'), nullable=False)
    title = Column(String, nullable=False)
    

class Writer(base):
    __tablename__ = 'Writer'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    
class Chat(base):
    __tablename__ = 'Chat'
    
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    w_time = Column(String, nullable=False)
    writer_id = Column(Integer, ForeignKey('Writer.id'), nullable=False)
    url_id = Column(Integer, ForeignKey('Url.id'), nullable=False)
    
    
class Jamack(base):
    __tablename__ = 'Jamack'
    
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    j_time = Column(String, nullable=False)
    url_id = Column(Integer, ForeignKey('Url.id'), nullable=False)
    


# In[57]:


base.metadata.create_all(engine)


# In[24]:


def insert_url(url, bj):
    """
        URL을 DB에 netloc과 path, param을 분해하여 저장하는 함수
        
        Parameter
        ----------
        url : 통 url을 넣으면 파싱해서 netloc, path, param 나눠서 저장해줍니다.
        bj: bj 이름(닉네임 or 아이디를 넣어주세요)
        
        Return
        ----------
        url.id(인덱스값)
        
    """
    
    parse = requests.compat.urlparse(url)
    netloc = parse[0]+"://"+parse[1]
    
    # netloc 이미 있는지 검사하고 없으면 추가하고 있으면 가져오기
    try:
        netloc1 = session.query(Netloc).filter(Netloc.netloc==netloc).one()
    except:
        netloc1 = Netloc(netloc=netloc)
        session.add(netloc1)
        session.commit()
        
    #bj 이미 있는지 검사하고 없으면 추가하고 있으면 가져오기
    try:
        bj1 = session.query(Bj).filter(Bj.name==bj).one()
    except Exception as e:
        bj1 = Bj(name=bj,netloc_id=netloc1.id, blacklist=False)
        session.add(bj1)
        session.commit()
        
    # url 처음 등록하는 것을 등록한다.
    try:
        url1 = session.query(Url).filter(Url.netloc_id==1)        .filter(Url.path==parse[2])        .filter(Url.param==parse[4]).one()
    except:
        url1 = Url(netloc_id=netloc1.id, path=parse[2], param=parse[4], bj_id=bj1.id, title='보겸tv')
        session.add(url1)
        session.commit()
        
    return url1.id


# 채팅 데이터 가져오기

# In[54]:


def insert_chat(chatdata, url_id):
    """
        Chatting 데이터 DB에 저장
        chatdata = (content, writer, time)
        
        Parameter
        ----------
        chatdata : list of (list or tuple) 채팅 데이터
        url_id : chatting 데이터 원본의 url_id
    """
    # 기존의 등록된 사용자(채팅작성자) 목록 가져오기
    writers_obj = session.query(Writer).all()
    writers = [_.name for _ in writers_obj]

    # 등록된 사람, 안된사람 합쳐서 chatdata와 같은 순서로 Writer 객체 만들고 db에 등록되어있는지 아닌지 확인
    writerList = [ (writers_obj[writers.index(w[1])], True) if w[1] in writers else (Writer(name=w[1]), False) for w in chatdata]

    # chat 등록
    chatList = []
    for i in range(len(chatdata)):
        if writerList[i][1]: # writer가 등록되어있는 경우
            chatList.append(Chat(content=chatdata[i][0], writer_id=writerList[i][0].id,
                w_time=chatdata[i][2], url_id=url_id))
        else: # writer가  등록되어있지 않은 경우 작성자를 먼저 디비에 저장해주고 진행
            session.add(writerList[i][0])
            session.commit()
            chatList.append(Chat(content=chatdata[i][0], writer_id=writerList[i][0].id,
                w_time=chatdata[i][2], url_id=url_id))

    session.add_all(chatList)
    session.commit()


# In[ ]:


def insert_urlchat(url, bj, chatdata):
    """
       채팅 저장 함수
       
        Parameter
        ----------
        url : 통 url을 넣으면 파싱해서 netloc, path, param 나눠서 저장해줍니다.
        bj: bj 이름(닉네임 or 아이디를 넣어주세요)
        chatdata : list of (list or tuple) 채팅 데이터
    """
    url_id = insert_url(url, bj)
    insert_chat(chatdata, url_id)
    


# In[ ]:


def insert_urljamack(url, bj, jamack):
    """
        자막 저장 함수
        
        Parameter
        -----------
        url: 통 url http://~~~~~
        bj: 비제이 아이디
        jamack : (content, j_time)튜플(or리스트)들이 들어있는 리스트 형태
        
    """
    url_id = insert_url(url, bj)
    session.add_all([Jamack(content=j[0], j_time=j[1], url_id=url_id) for j in jamack])
    
    

