from flask import Flask, render_template, redirect, request, url_for, flash
import pymysql

import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
import librosa.display

import numpy as np
import os

from siamese import train, test

app = Flask(__name__)
app.secret_key = 'serseas'

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/page')
def page():
    return render_template('page.html')

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
        train()
        return redirect(url_for('login'))
    return render_template('sign.html')
    

@app.route('/sign/img', methods = ['GET', 'POST'])
def signimg():
    if request.method == 'POST':
        sign_file('voice')
    return render_template('sign.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
        elif os.path.exists('./test/' + id + '.png') == False:
            flash("음성을 녹음해주세요.")
        else:
            if(test(id) == id):
                return redirect(url_for('page'))
            else:
                flash("로그인 실패!!")
            os.remove('./test/' + id + '.png')  # 로그인 파일 제거
    return render_template('login.html')


@app.route('/login/img', methods=['GET', 'POST'])
def loginimg():
    if request.method == 'POST':
        login_file('voice')
    return render_template('login.html')


def sign_file(value):
    file = request.files[value]  # blob 파일 저장

    os.makedirs('./train/' + file.filename, exist_ok=True)  # 폴더 생성

    file.save(os.path.join('./train/' + file.filename,
                           file.filename + '.wav'))  # 폴더 위치에 파일 저장

    audio_path = './train/' + file.filename + '/' + file.filename + '.wav'  # 오디오 파일 경로


    # wav plot 이미지
    y, sr = librosa.load(audio_path)  # lbrosa.load() : 오디오 파일을 로드한다.

    ipd.Audio(y, rate=sr)

    plt.figure(figsize=(16, 6))
    librosa.display.waveshow(y=y, sr=sr)
    plt.plot(y)

    # MFCC 이미지 
    # # min_level_db= -100 
    # # def normalize_mel(S):
    # #     return np.clip((S-min_level_db)/-min_level_db,0,1)


    # # def feature_extraction(path):
    # #     y, sr = librosa.load(path)
    # #     S =  librosa.feature.melspectrogram(y=y, n_mels=80, n_fft=512, win_length=400, hop_length=160) # 320/80
    # #     norm_log_S = normalize_mel(librosa.power_to_db(S, ref=np.max))
    # #     return norm_log_S
                                

    # a = feature_extraction(audio_path)

    # librosa.display.specshow(a)  

    # plt.tight_layout()

    if os.path.exists('./train/' + file.filename + '/' + file.filename + ".png") == True:  # 파일 중복시
        plt.savefig('./train/' + file.filename + '/' +
                    file.filename + '(1)' + ".png")
    else:
        plt.savefig('./train/' + file.filename + '/' +
                    file.filename + ".png")  # png 파일 저장

    os.remove('./train/' + file.filename + '/' +
              file.filename + '.wav')  # 음성 파일 제거


def login_file(value):
    file = request.files[value]  # blob 파일 저장

    if (os.path.isdir('./train/' + file.filename) == True):
        file.save(os.path.join('./test',
                               file.filename + '.wav'))  # 폴더 위치에 파일 저장

        audio_path = './test/' + file.filename + '.wav'  # 오디오 파일 경로

        # wav plot 이미지
        y, sr = librosa.load(audio_path)  # lbrosa.load() : 오디오 파일을 로드한다.

        ipd.Audio(y, rate=sr)

        plt.figure(figsize=(16, 6))
        librosa.display.waveshow(y=y, sr=sr)
        plt.plot(y)

        # MFCC 이미지 
        # # min_level_db= -100 
        # # def normalize_mel(S):
        # #     return np.clip((S-min_level_db)/-min_level_db,0,1)


        # # def feature_extraction(path):
        # #     y, sr = librosa.load(path)
        # #     S =  librosa.feature.melspectrogram(y=y, n_mels=80, n_fft=512, win_length=400, hop_length=160) # 320/80
        # #     norm_log_S = normalize_mel(librosa.power_to_db(S, ref=np.max))
        # #     return norm_log_S
                                    

        # a = feature_extraction(audio_path)

        # librosa.display.specshow(a)  

        # plt.tight_layout()

        plt.savefig('./test/' +
                    file.filename + ".png")  # png 파일 저장

        os.remove('./test/' +
                  file.filename + '.wav')  # 음성 파일 제거
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
