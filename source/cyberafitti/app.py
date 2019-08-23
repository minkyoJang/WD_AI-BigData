from flask import Flask, render_template, request
from run_model import run_model

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    # return render_template('youtube.html')
    return render_template('prepare.html')


@app.route('/afreeca', methods=['GET', 'POST'])
def afreeca():
    # return render_template('afreeca.html')
    return render_template('prepare.html')


@app.route('/twitch', methods=['GET', 'POST'])
def twitch():
    # return render_template('twitch.html')
    return render_template('prepare.html')


@app.route('/model')
def model():
    return render_template('model.html')


@app.route('/download')
def download():
    return render_template('download.html')


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == "POST":
        query = request.form.get('query')
        result = "%.3f" % run_model(query)
        return result
    else:
        return render_template('demo.html')


if __name__ == '__main__':
    app.run()
