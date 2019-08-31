from flask import Flask, render_template, request, url_for
import run_model
from attention.attention_model import StructuredSelfAttention
import threading
from flask_sqlalchemy import SQLAlchemy
import vod_url_scrapping as vod
from model import Bj, Platform
from sqlalchemy import and_, or_, create_engine
from sqlalchemy.orm import sessionmaker
import json
from collections import defaultdict
import pandas as pd
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///server.db"
db = SQLAlchemy()
db.init_app(app)

# server.db에는 table이 2개 입니다. bj와 platform

# 현재 프로그램이 돌아가는 방식은 서버가 시작되고 첫 request가 들어오면 스레드가 실행되며
# db에 있는 유해도를 확인하지 않은 bj에 대하여 url(차단 파일에 들어가는 형식 ex) /234567, /watch=kljaooo)을 파싱해 옵니다
# 파싱해 온 영상에서 3개의 채팅 데이터를 스크래핑 해와서 DataFrame 1개로 합친 후 csv로 저장합니다.
# 이 DataFrame을 model에 넣어 유해도를 측정합니다
# 유해하다면 blacklist.txt(유해한 bj의 url, 영상 url들을 저장합니다.)에 저장을 하고 모든 bj들에 확인이 끝났다면
# 차단 파일을 생성합니다.


@app.before_first_request
def first_strat():
    Session = sessionmaker(bind=create_engine('sqlite:///server.db'))
    # with open('./data/blacklist.json', 'w') as f:
    #     json.dump(defaultdict(str), f)
    # 테스트 용으로 1회 실행되는 스레드입니다.
    # threading.Thread(target=run, args=[Session(), Bj, Platform]).start()
    # 7일마다 이 함수를 실행한다.(반복 실행)
    # threading.Timer(60.0*60.0*24*7,run).start()


def run(session, Bj, Platform):
    # 확인하지 않은 bjList [(bj_id, platform)]을 가져와서
    # bjList = [(_.name, _.platform.name) for _ in session.query(Bj).filter_by(seen=0).all()]
    bjList = [(_.name, _.platform.name) for _ in session.query(Bj).filter_by(seen=0).all()][:1]
    print(bjList)

    # 영상들의 url을 파싱해오고
    urlDict = vod.parse_url(bjList)
    print(urlDict.keys())
    print('urlDict=', len(urlDict))

    # 파싱해온 n개의 url에서 data를 긁어와서 pandas DataFrame 형태로 만들어준다.
    # 파싱하는 중간중간 영상 1개에 대해서 파싱 끝나면 채팅 데이터 파일로 저장하게 하는 것이 좋을 거 같습니다
    # 영상 하나하나 유해도 판단하는거 테스트 코드
    for urlList, bj_pl in zip(urlDict.values(), bjList):
        print("urlList = ", urlList)
        # if len(urlList) < 3:
        #     continue
        bj, platform = bj_pl
        print(platform, type(platform))
        print('bj={}, platform={}'.format(bj, platform))
        data = vod.make_dataset(urlList, platform, len(urlList)) # 모든 영상 검사
        # data = vod.make_dataset(urlList, platform, 3) # 영상 3개 검사 -> 마지막 파라미터 조절해서 검사 가능
        print("data.len = ", len(data))
        print(data.keys())



        # 파일로 저장해주고
        data.to_csv('./data/chat'+bj+'('+platform+')'+'.csv')

        # 모델에 전달해준다.
        # result = run_model(data['content']) # 채팅 데이터가 data['content']
        result = []
        for u in urlList:

            if len(data[data['url'] == u]) > 0:
                tmp = run_model.RunAttentionModel(data[data['url'] == u]['content'])
                tmp.predict()
                result.append(int(tmp.run_bj()*100))
            else:
                result.append('unkown')

        if platform == 'twitch':
            urlList = [_ for _ in urlList]
        check_result = [ _ for _ in result if type(_) is int] # 확인한 영상에 대하여 평균을 낸다(bj유해도)
        platform_id = session.query(Platform).filter_by(name=platform).first().id
        bj_db = session.query(Bj).filter(and_(Bj.name == bj, Bj.platform_id == platform_id)).first()
        if len(check_result) == 0:
            bj_db.seen = 1
            session.commit()
            continue
        bj_result = sum(check_result)/len(check_result)
        # print("result=", result)
        # print("bj_result=", bj_result)

        # 받은 결과로 유해하다면 db에 blacklist를 1로 변환하고, blockUrl_list.js파일로 만들어 저장해준다.
        if bj_db.platform_id != 1: # 유튜브가 아니면 /bj_id도 추가해주어야 함.
            urlList.append("/"+bj) # /bj아이디 형식도 차단 목록에 넣어 주어야 함. -> 유튜브는 다르다.
            result.append(bj_result)
        if bj_result >= 8:
            print('유해!!!!!!!!')
            bj_db.blacklist = 1
            # 블랙 리스트라면 이 사람의 영상들 url 목록을 기존 차단 파일에 추가해준다.
            with open('./data/blacklist.json', 'r') as f:
                blacklist = json.load(f)


            for k, v in zip(urlList, result):
                blacklist[k] = v
            with open('./data/blacklist.json', 'w') as f:
                json.dump(blacklist, f)


        # 확인한 bj에 대하여 seen을 1로 바꿔준다.
        bj_db.seen=1
        bj_db.per = bj_result
        session.commit()

    # bj들에 대하여 유해도 판단이 끝나면 저장되어있는 차단url 목록을 불러와서 차단 파일(blockUrl_list.js)를 생성합니다.
    with open('./data/blacklist.json', 'r') as f:
        blackList = json.load(f)
    print(blackList)
    with open('./data/blockUrl_list.js', 'w') as f:
        f.write("let blockUrls=")
        json.dump(blackList,f)

    session.close() # 스레드가 끝나면 session을 잘 정리해주자!


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/introduce')
def introduce():
    black = [(i+1, _.nick, _.platform_id, _.per) for i, _ in
             enumerate(Bj.query.filter_by(blacklist=1).order_by(Bj.per.desc()).limit(10).all())]
    if black:
        mapper = {1: '유튜브', 2: '아프리카tv', 3: "트위치"}
        black = pd.DataFrame(black)
        black[2] = black[2].map(mapper)
        black[3] = black[3].astype({3:'int'})
        black = black.values

    return render_template('introduce.html', black=black)


@app.route('/download')
def download():
    return render_template('download.html')


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == "POST":
        query = request.form.get('query')
        demoTmp = run_model.RunAttentionModel([query])
        demoTmp.predict()
        result = demoTmp.run_demo()[0][0]
        result = int(result * 100)
        script = demoTmp.visualize()
        return render_template("Ndemo.html", result=result, script=script)
    else:
        return render_template('Ndemo.html')


stream = defaultdict(lambda: defaultdict(lambda:[0,0]))

@app.route('/mandoo', methods=["POST"])
def mandoo():
    # 주소가 오면 받아서 blacklist에 있는 것인지 확인하고 있으면(어차피 차단될것) 아무것도 반환 안 하고
    # 블랙리스트에 없으면
    # 파싱해서 유해도 산출한 후 유해하면 전송 {"차단url":유해도}
    # 실시간용(스트리밍용)

    res = json.loads(request.form.get('chat')) # chat
    user = res['private']
    url = res['url']
    chat = res["chat"]
    print("private = {}, url = {}, chat = {}".format(user, url, chat))
    if "http" in url:
        url = requests.compat.urlparse(url)[2]
        st = stream[user][url]
        if st[1] > 100:
            st[0], st[1] = 0, 0
        tmp = run_model.RunAttentionModel([chat])
        tmp.predict()
        result = int(tmp.run_demo()*100)
        print("result = ", result)
        st[1] += 1
        if result > 49: # 50% 이상이면 유해한 채팅
            st[0] += 1
            print("욕설 : {}, 채팅수 : {}".format(st[0], st[1]))
        if st[0] > 2: # 100개중 18개 이상 나오면 유해하다 판단하고 차단(시연 때 빠른 차단을 보여주기위해서 잠시 줄임)
            per = int(st[0] / st[1] * 100)
            return '{"' + url + '":' + str(per) + '}'
        else:
            return "N"
    else:
        return "N"


    # 기존에 있는 영상 채팅/ 자막 가져옴
    # print("query = ", query)
    # platform, url = parseUrl(query)
    # print('platform = ', platform)
    # print('url = ', url)
    # if platform == '' or url == '' :
    #     return 'N'
    # # 블랙리스트 확인 --> 서버 터질 우려 있음 매번 열면...
    # # 주기적으로 업데이트 해주고 전역변수로 만들어야 할 듯
    # with open('./data/blacklist.json', 'r') as f:
    #     blacklist = json.load(f)
    #
    # # 이미 블랙리스트에 있으면 N 반환
    # if url in blacklist:
    #     return 'N'
    #
    # # 없으면 채팅 긁어와서 모델을 돌리고 유해도 판정하여 반환
    # try:
    #     data = vod.make_dataset([url], platform, n=1)
    #     print("파싱 완료", data.shape)
    #     tmp = run_model.RunAttentionModel(data)
    #     tmp.predict()
    #     result = int(tmp.run_bj()*100)
    #     print("result = ",result);
    #     # result = 12;
    #     if result >= 8:
    #         print(json.dumps({url:result}))
    #         return json.dumps({url:result})
    #     else:
    #         return 'N'
    # except:
    #     print("error 발생")
    #     return 'N' # 에러발생(못찾거나 등등 이면 N을 반환해줄거임



@app.errorhandler(403)
def error404(err):
    return render_template('error/403.html')


@app.errorhandler(404)
def error404(err):
    return render_template('error/404.html')


@app.errorhandler(500)
def error500(err):
    return render_template('error/500.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000")
