from flask import Flask, render_template, request, url_for
from run_model import run_model
import threading
from flask_sqlalchemy import SQLAlchemy
import vod_url_scrapping as vod
from model import Bj, Platform
from sqlalchemy import and_, or_, create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///server.db"
db = SQLAlchemy()
db.init_app(app)

# server.db에는 table이 2개 입니다. bj와 platform
# bj table에 유해도 %를 저장할 column 추가 필요합니다.

# 현재 프로그램이 돌아가는 방식은 서버가 시작되고 첫 request가 들어오면 스레드가 실행되며
# db에 있는 유해도를 확인하지 않은 bj에 대하여 url(차단 파일에 들어가는 형식 ex) /234567, /watch=kljaooo)을 파싱해 옵니다
# 파싱해 온 영상에서 3개의 채팅 데이터를 스크래핑 해와서 DataFrame 1개로 합친 후 csv로 저장합니다.
# 이 DataFrame을 model에 넣어 유해도를 측정합니다
# 유해하다면 blacklist.txt(유해한 bj의 url, 영상 url들을 저장합니다.)에 저장을 하고 모든 bj들에 확인이 끝났다면
# 차단 파일을 생성합니다.


@app.before_first_request
def first_strat():
    Session = sessionmaker(bind=create_engine('sqlite:///server.db'))

    # 테스트 용으로 1회 실행되는 스레드입니다.
    # threading.Thread(target=run, args=[Session(), Bj, Platform]).start()
    # 7일마다 이 함수를 실행한다.(반복 실행)
    # threading.Timer(60.0*60.0*24*7,run).start()


def run(session, Bj, Platform):
    # 확인하지 않은 bjList [(bj_id, platform)]을 가져와서
    bjList = [(_.name, _.platform.name) for _ in session.query(Bj).filter_by(seen=0).all()]
    print(bjList)

    # 영상들의 url을 파싱해오고
    urlDict = vod.parse_url(bjList)
    print(urlDict[0])
    print('urlDict=', len(urlDict))

    # 파싱해온 n개의 url에서 data를 긁어와서 pandas DataFrame 형태로 만들어준다.
    # 파싱하는 중간중간 영상 1개에 대해서 파싱 끝나면 채팅 데이터 파일로 저장하게 하는 것이 좋을 거 같습니다
    for urlList, bj_pl in zip(urlDict.values(), bjList):
        print("urlList = ", urlList)
        if len(urlList) < 3:
            continue
        bj, platform = bj_pl
        print(platform, type(platform))
        print('bj={}, platform={}'.format(bj, platform))
        data = vod.make_dataset(bj, urlList, platform, 3)
        print("data.len = ", len(data))
        print(data.keys())



        # 파일로 저장해주고
        data.to_csv('./data/'+bj+'('+platform+')'+'.csv')

        # 모델에 전달해준다.
        result = run_model(data[0])
        print("result=", result)

        # 받은 결과로 유해하다면 db에 blacklist를 1로 변환하고, blockUrl_list.js파일로 만들어 저장해준다.
        platform_id = session.query(Platform).filter_by(name=platform).first().id
        bj_db = session.query(Bj).filter(and_(Bj.name==bj, Bj.platform_id==platform_id)).first()
        urlList.append("/"+bj) # /bj아이디 형식도 차단 목록에 넣어 주어야 함. -> 유튜브는 다르다.
        if result*100 >= 8:
            print('유해!!!!!!!!')
            bj_db.blacklist = 1
            # 블랙 리스트라면 이 사람의 영상들 url 목록을 기존 차단 파일에 추가해준다.
            with open('./data/blacklist.txt', 'a') as f:
                [f.write('"'+url+'",') for url in urlList]

        # 확인한 bj에 대하여 seen을 1로 바꿔준다.
        bj_db.seen=1
        session.commit()
        print('1명 완료!')

    # bj들에 대하여 유해도 판단이 끝나면 저장되어있는 차단url 목록을 불러와서 차단 파일(blockUrl_list.js)를 생성합니다.
    with open('./data/blacklist.txt', 'r') as f:
        blackList = f.read()
    print(blackList)
    with open('./data/blockUrl_list.js', 'w') as f:
        f.write("let blockUrls=[" + blackList + "];")

    session.close() # 스레드가 끝나면 session을 잘 정리해주자!


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    # return render_template('youtube.html')
    return render_template('youtube.html')


@app.route('/afreeca', methods=['GET', 'POST'])
def afreeca():
    # return render_template('afreeca.html')
    return render_template('prepare.html')


@app.route('/twitch', methods=['GET', 'POST'])
def twitch():
    # return render_template('twitch.html')
    return render_template('prepare.html')


@app.route('/model')
def information():
    return render_template('information.html')


@app.route('/download')
def download():
    return render_template('download.html')


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == "POST":
        query = list(request.form.get('query'))
        print(query)
        result = run_model(query)
        print("result = ", result)
        result = "%.3f" % result
        print("str result = ",result)
        return result
    else:
        return render_template('Ndemo.html')

# @app.route('/demo')
# def demo():
#     return render_template('Ndemo.html')



if __name__ == '__main__':
    app.run()
