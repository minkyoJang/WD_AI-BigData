#!/usr/bin/env python
# coding: utf-8

import requests
from collections import defaultdict
import json
import re
from scrapChat import afre_chat, twi_chat, youtube_jamak
import pandas as pd
from download import download
from bs4 import BeautifulSoup


def afreeca_get_video_urls(bj_id):
    """
    아프리카 비제이의 영상 url들을 파싱해오는 함수 입니다.

    :param bj_id: bj의 아이디 입니다.(닉네임x)
    :return: 아프리카 비제이의 영상 url (/123453형식)을 반환합니다.
    """
    url='http://bjapi.afreecatv.com/api/'+bj_id+'/vods'
    video_list = []
    i = 1
    while True:
        param = {'page':i}
        result = download('get', url, param=param).json()['data']
        if not result:
            break
        video_list.extend([str(_['title_no']) for _ in result])
        i += 1
    return video_list


# In[74]:

def get_video_urls(bj_id, platform):
    """
    플랫폼별로 불러오는 방식이 달라 bj_id와 platform을 입력하면 그에 맞춰 처리해줍니다.
    :param bj_id: bj_id
    :param platform: 플랫폼 이름(영어)를 넣어주세요
    :return: bj의 영상 url들을 반환해줍니다.
    """
    if platform == 'afreeca':
        return afreeca_get_video_urls(bj_id)
    elif platform == 'twitch':
        return twitch_get_video_urls(bj_id)
    else:
        return youtube_get_video_urls(bj_id)


def parse_url(bjList):
    """
    비제이들의 영상 url 목록들을 파싱하는 함수
    
    Parameters
    ----------
    bjList : list형태, 영상 링크들을 파싱해오고 싶은 비제이 아이디가 들어있는 리스트
    get_video_urls : function, 파싱하고 싶은 사이트의 url을 파싱해오는 함수

    :return: {'bj_id':['/urls',...]} dict형식으로 여러 bj들의 url list를 반환해줍니다.
    """
    urldict = defaultdict(list)
    for bj_id, platform in bjList:
        vUrls = get_video_urls(bj_id, platform)
        urldict[bj_id] = vUrls
        print('1명꺼 끝!')
    return urldict


# In[75]:


def twitch_get_video_urls(bj_id):
    """
    트위치 비제이의 영상 목록을 파싱해오는 함수
    :param bj_id: str, bj의 아이디를 입력
    :return: list, url들이 들어있는 list
    """
    data = {"operationName": "FilterableVideoTower_Videos",
            "variables": {"limit": 30, "channelOwnerLogin": bj_id, "broadcastType": None, "videoSort": "TIME"},
            "extensions": {"persistedQuery": {"version": 1,
                                              "sha256Hash": "2023a089fca2860c46dcdeb37b2ab2b60899b52cca1bfa4e720b260216ec2dc6"}}}
    lst = []
    while True:
        data1 = json.dumps(data)
        html = download("post", "https://gql.twitch.tv/gql", data=data1)
        dom = html.json()
        dom['data']['user']['videos']['edges'][len(dom['data']['user']['videos']['edges']) - 1]
        lst.extend(['/' + _['node']['id'] for _ in dom['data']['user']['videos']['edges']])
        if dom['data']['user']['videos']['pageInfo']['hasNextPage'] == True:
            data['variables']['cursor'] = \
            dom['data']['user']['videos']['edges'][len(dom['data']['user']['videos']['edges']) - 1]['cursor']
        else:
            break

    return lst


# json, requests, BeautifulSoup, re
def youtube_get_video_urls(bj_id):
    """
    youtube bj_id를 받아서 영상의 url을 파싱해오는 함수(채널로 되어있는거 적용 o)
    :param bj_id: str
    :return: list, ex) ['/watch?v=aAKC8AD']
    """
    # request.session을 사용한다.
    session = requests.session()

    # 유튜브를 스크래핑 할 때 필요한 쿠키들을 저장해 놓은 것을 불러온다.
    with open('./data/youtube_cookies.cks', 'r') as f:
        cookies = json.loads(f.read())

    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])

    domain = 'https://www.youtube.com'  # 도메인 주소
    url = domain + bj_id + '/videos'  # 시작 주소
    urlList = []

    while True:
        html = session.get(url)
        if 'browse_ajax' in url:
            dom = BeautifulSoup(html.json()['content_html'], 'lxml')
        else:
            dom = BeautifulSoup(html.text, 'lxml')

        urls = [_['href'] for _ in
                dom.select('h3.yt-lockup-title a.yt-uix-sessionlink.yt-uix-tile-link')]

        urlList.extend(urls)

        if 'browse_ajax' in url:
            target = html.json()['load_more_widget_html']
            if not target:
                break
            dom = BeautifulSoup(target, 'lxml')

        nextUrl = dom.select_one('.load-more-button.yt-uix-button')['data-uix-load-more-href']
        url = domain + nextUrl

    return urlList


def afreeca_make_datasets(urls, n=3):
    '''
    파싱해온 urls를 넣으면 영상 3개에서 chatingdata를 뽑아온다.
    :param bj_id: str
    :param urls: list, url = '123345'
    :param n: 채팅 데이터를 스크래핑할 영상 개수 default = 3
    :return: DataFrame, columns = [0, 1, 2] : (comment, writer, time)
    '''
    result = pd.DataFrame()
    for _ in urls[:n]:
        url = 'http://vod.afreecatv.com/PLAYER/STATION/' + _
        chatdata = pd.DataFrame(afre_chat(url))
        chatdata['url'] = _
        result = pd.concat([result, chatdata])

    result.rename(columns = {0: 'content', 1: 'writer', 2: 'time'}, inplace=True)
    return result.reset_index()


def twitch_make_datasets(urls, n=3):
    '''
    트위치 영상 채팅 데이터 스크래핑 하는 함수
    :param bj_id: str, bj 아이디
    :param urls: list, '/123435'형태의 url이 들어있는 list
    :param n: int, 스크래핑 하고 싶은 영상 개수 (default=3)
    :return: DataFrame, columns = (content, writer, time, url)
    '''
    result = pd.DataFrame()
    for _ in urls[:n]:
        chatdata = pd.DataFrame(twi_chat(_))
        chatdata['url'] = _
        result = pd.concat([result, chatdata])

    result.rename(columns = {0:'content', 1:'writer', 2:'time'}, inplace=True)
    return result.reset_index()


def youtube_make_datasets(urls, n=3):
    '''
    파싱해온 urls를 넣으면 영상 3개에서 chatingdata를 뽑아온다.
    :param bj_id: str
    :param urls: list, url = '/123345'
    :param n: 채팅 데이터를 스크래핑할 영상 개수 default = 3
    :return: DataFrame, columns = content, url
    '''
    result = pd.DataFrame()
    for _ in urls[:n]:
        chatdata = pd.DataFrame(youtube_jamak(_))
        chatdata['url'] = _
        result = pd.concat([result, chatdata])

    result.rename(columns={0:'content'}, inplace=True)
    return result.reset_index()


def make_dataset(urls, platform, n=3):
    '''
    플랫폼을 같이 받아서 데이터 셋을 만들어주는 함수
    :param bj_id: str, bj 아이디
    :param urls: list, '/123435'형태의 url이 들어있는 list
    :param platform: str,
    :param n: int, 스크래핑 하고 싶은 영상 개수 (default=3)
    :return: DataFrame, columns = [0, 1, 2] : (comment, writer, time)
    '''
    print('platform = ', platform)
    if platform =='afreeca':
        return afreeca_make_datasets(urls, n)
    elif platform =='twitch':
        return twitch_make_datasets(urls, n)
    else :
        return youtube_make_datasets(urls, n)