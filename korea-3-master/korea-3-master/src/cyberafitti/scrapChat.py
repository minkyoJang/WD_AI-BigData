from download import download
from bs4 import BeautifulSoup
from requests.compat import urlparse
from xml.etree import ElementTree
import numpy
import requests
import re


def afre_chat(url):
    '''
    return chatting log numpy array
    '''

    try:
        html = download('get', url)  # 파싱 동영상 url
        dom = BeautifulSoup(html.text, 'lxml')  # dom화
        metatag = dom.select_one("meta[property='og:image']")['content']  # key찾는 과정
        rowKey = urlparse(metatag).query  # key만 가져옴
        key = rowKey[:-1] + 'c'  # url 변경
        # xml request
        xml = download('get', 'http://videoimg.afreecatv.com/php/ChatLoad.php', param=key)
        xmltree = ElementTree.XML(xml.text)  # xml tree화

        # nickname / id / chat / time 의 n
        chatdata = numpy.asarray(tuple(zip(map(lambda x: x.text, xmltree.findall('chat/m')),
                                           map(lambda x: x.text,
                                               xmltree.findall('chat/u')),
                                           map(lambda x: x.text, xmltree.findall('chat/t')))))
    except:
        chatdata = numpy.asarray([[]])

    return chatdata


def twi_chat(url):
    '''
    트위치 영상 url중 끝 부분을 전달해주면 채팅을 파싱해오는 함수
    :param url: ex) /2633849
    :return:
    '''
    chatdata = []
    url = 'https://api.twitch.tv/v5/videos'+url+'/comments'
    param = {
        'content_offset_seconds':0
    }
    while True:
        res = download('get',url, param=param).json()
        chatdata.extend([(_['message']['body'], _['commenter']['name'], _['content_offset_seconds'])
                         for _ in res['comments']])
        if '_next' not in res.keys():
            break
        param = {
            'cursor':res['_next']
        }
    return chatdata



def youtube_jamak(url_id):
    url = "https://www.youtube.com"+url_id
    html = download('get', url)
    dom = BeautifulSoup(html.text, 'lxml')
    if len([_.text for _ in dom.select('script') if 'captionTracks' in _.text]) <= 0:
        return None
    else:
        target = [_.text for _ in dom.select('script') if 'captionTracks' in _.text][0]
        target = re.sub(r'\\','', target)
        target = re.sub(r'u0026', '&', target)
        capUrl = re.search(r'\{\"captionTracks\":\[\{\"baseUrl\"\:\"(.+)\",\"n',target).group(1)
        capUrl = re.sub(r'&lang=(.+)', '&lang=ko', capUrl)
        cap = download('get', capUrl)
        caption = cap.text
        caption = re.sub(r'&lt;','<',caption)
        caption = re.sub(r'&gt;', '>', caption)
        cDom = BeautifulSoup(caption, 'lxml')
        return [_.text for _ in cDom.select('text')]




