from flask import Flask, render_template, redirect, request, url_for
import pymysql
from werkzeug.utils import secure_filename

import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
import librosa.display

import os

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/sign', methods=['GET', 'POST'])  # 회원가입 -> 디비 저장
def sign():
    # db = pymysql.connect(host='localhost', port=3306, user='hyemin',
    #                      password='1234', db='user', charset='utf8')
    # cursor = db.cursor()
    if request.method == 'POST':
        sign_file('voice')

        # id = request.form.get('id')
        # passwd = request.form.get('passwd')
        # voice = id+'.png'
        # sql = "INSERT INTO user (id, pass, voice) VALUES (%s, %s, %s)"
        # cursor.execute(sql, (id, passwd, voice))
        # db.commit()
        return redirect(url_for('login'))
    return render_template('sign.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_file('voice')
    return render_template('login.html')


def sign_file(value):
    file = request.files[value]  # blob 파일 저장

    os.makedirs('./' + file.filename, exist_ok=True)  # 폴더 생성

    file.save(os.path.join('./' + file.filename,
                           secure_filename(file.filename) + '.wav'))  # 폴더 위치에 파일 저장

    audio_path = './' + file.filename + '/' + file.filename + '.wav'  # 오디오 파일 경로

    y, sr = librosa.load(audio_path)  # lbrosa.load() : 오디오 파일을 로드한다.

    print(y)
    print(len(y))
    print('Sampling rate (Hz): %d' % sr)
    print('Audio length (seconds): %.2f' %
          (len(y) / sr))  # 음악의 길이(초) = 음파의 길이/Sampling rate

    ipd.Audio(y, rate=sr)

    plt.figure(figsize=(16, 6))
    librosa.display.waveshow(y=y, sr=sr)
    plt.plot(y)

    print(os.path.exists('./' + file.filename + '/' + file.filename + ".png"))

    if os.path.exists('./' + file.filename + '/' + file.filename + ".png") == True:  # 파일 중복시
        plt.savefig('./' + file.filename + '/' +
                    file.filename + '(1)' + ".png")
    else:
        plt.savefig('./' + file.filename + '/' +
                    file.filename + ".png")  # png 파일 저장

    os.remove('./' + file.filename + '/' +
              file.filename + '.wav')  # 음성 파일 제거


def login_file(value):
    file = request.files[value]  # blob 파일 저장

    if (os.path.isdir('./' + file.filename) == True):
        file.save(os.path.join('./' + file.filename,
                               secure_filename(file.filename) + '.wav'))  # 폴더 위치에 파일 저장

        audio_path = './' + file.filename + '/' + file.filename + '.wav'  # 오디오 파일 경로

        y, sr = librosa.load(audio_path)  # lbrosa.load() : 오디오 파일을 로드한다.

        print(y)
        print(len(y))
        print('Sampling rate (Hz): %d' % sr)
        print('Audio length (seconds): %.2f' %
              (len(y) / sr))  # 음악의 길이(초) = 음파의 길이/Sampling rate

        ipd.Audio(y, rate=sr)

        plt.figure(figsize=(16, 6))
        librosa.display.waveshow(y=y, sr=sr)
        plt.plot(y)
        plt.savefig('./' + file.filename + '/' +
                    file.filename + "(1).png")  # png 파일 저장

        os.remove('./' + file.filename + '/' +
                  file.filename + '.wav')  # 음성 파일 제거


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
