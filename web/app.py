from flask import Flask, render_template, redirect, request, url_for, flash
import pymysql

import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
import librosa.display

import os

from siamese import train

app = Flask(__name__)
app.secret_key = 'serseas'

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    db = pymysql.connect(host='localhost', port=3306, user='nemin',
                         password='1234', db='voice', charset='utf8')
    cursor = db.cursor()
    if request.method == 'POST':
        id = request.form.get('id')
        passwd = request.form.get('passwd')
        voice1 = id+'.png'
        voice2 = id+'(1).png'
        sql = "INSERT INTO voiceInfo (id, pass, voice1, voice2) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql, (id, passwd, voice1, voice2))
        db.commit()
        return redirect(url_for('login'))
    return render_template('sign.html')
    

@app.route('/sign/img', methods = ['GET', 'POST'])
def signimg():
    if request.method == 'POST':
        sign_file('voice')
    return render_template('sign.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    train()
    if request.method == 'POST':
        db = pymysql.connect(host='localhost', port=3306, user='nemin',
                         password='1234', db='voice', charset='utf8')
        cursor = db.cursor()
        id = request.form.get('id')
        sql = "select count(id) from voiceInfo where id = %s;"
        cursor.execute(sql, id)
        rows = cursor.fetchall()
        if rows[0][0] == 0:
            flash("아이디가 존재하지 않습니다.")

    return render_template('login.html')


@app.route('/login/img', methods=['GET', 'POST'])
def loginimg():
    if request.method == 'POST':
        login_file('voice')
    return render_template('login.html')


def sign_file(value):
    file = request.files[value]  # blob 파일 저장

    os.makedirs('./img/' + file.filename, exist_ok=True)  # 폴더 생성

    file.save(os.path.join('./img/' + file.filename,
                           file.filename + '.wav'))  # 폴더 위치에 파일 저장

    audio_path = './img/' + file.filename + '/' + file.filename + '.wav'  # 오디오 파일 경로

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

    if os.path.exists('./img/' + file.filename + '/' + file.filename + ".png") == True:  # 파일 중복시
        plt.savefig('./img/' + file.filename + '/' +
                    file.filename + '(1)' + ".png")
    else:
        plt.savefig('./img/' + file.filename + '/' +
                    file.filename + ".png")  # png 파일 저장

    os.remove('./img/' + file.filename + '/' +
              file.filename + '.wav')  # 음성 파일 제거


def login_file(value):
    file = request.files[value]  # blob 파일 저장

    if (os.path.isdir('./img/' + file.filename) == True):
        file.save(os.path.join('./img/' + file.filename,
                               file.filename + '_login.wav'))  # 폴더 위치에 파일 저장

        audio_path = './img/' + file.filename + '/' + file.filename + '_login.wav'  # 오디오 파일 경로

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
        plt.savefig('./img/' + file.filename + '/' +
                    file.filename + "_login.png")  # png 파일 저장

        os.remove('./img/' + file.filename + '/' +
                  file.filename + '_login.wav')  # 음성 파일 제거



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
