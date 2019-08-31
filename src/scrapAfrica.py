from download import download
from bs4 import BeautifulSoup
from requests.compat import urlparse
from xml.etree import ElementTree
import numpy


def get_chat(url):
    '''
    return chatting log numpy array
    '''

    html = download('get', url)  # 파싱 동영상 url
    dom = BeautifulSoup(html.text, 'lxml')  # dom화
    metatag = dom.select_one("meta[property='og:image']")['content']  # key찾는 과정
    rowKey = urlparse(metatag).query  # key만 가져옴
    key = rowKey[:-1]+'c'  # url 변경
    # xml request
    xml = download('get', 'http://videoimg.afreecatv.com/php/ChatLoad.php', param=key)
    xmltree = ElementTree.XML(xml.text)  # xml tree화

    # nickname / id / chat / time 의 n
    chatdata = numpy.asarray(tuple(zip(map(lambda x: x.text, xmltree.findall('chat/m')),
                                       map(lambda x: x.text,
                                           xmltree.findall('chat/u')),
                                       map(lambda x: x.text, xmltree.findall('chat/t')))))

    return chatdata
