from flask import Flask, render_template, request, send_file
from run_model import run_model
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('1_index.html')

@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    return render_template('youtube.html')

@app.route('/afreeca', methods=['GET', 'POST'])
def afreeca():
    return render_template('afreeca.html')

@app.route('/twitch', methods=['GET', 'POST'])
def twitch():
    return render_template('twitch.html')

@app.route('/model')
def model():
    return render_template('model.html')


# @app.route('/file_download', methods=['GET','POST'])
# def file_download():
#     return render_template('file_download.html')


@app.route('/download')
def download():
    return render_template('download.html')

# @app.route('/realdown', methods=['GET'])
# def real_download():
#     filepath=r"C:\Users\missr\PycharmProjects\CYBERA\static\downloadfile"
#     filename=r"ex_chroemExtension.zip"
#     return send_file(os.path.join(filepath,filename), as_attachment=True)

@app.route('/Ndemo', methods=['GET','POST'])
def Ndemo():
    if request.method == "POST":
        query = request.form.get('query')
        return render_template('Ndemo.html', predict=run_model(query))
    else:
        return render_template('Ndemo.html')




if __name__ == '__main__':
    app.run()
