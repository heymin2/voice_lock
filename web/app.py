from flask import Flask, render_template, redirect, request, url_for
import pymysql
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def voice():

    return render_template('voiceRecord.html')


@app.route('/sign', methods=['GET', 'POST'])  # 회원가입 -> 디비 저장
def sign():
    db = pymysql.connect(host='localhost', port=3306, user='hyemin',
                         password='1234', db='user', charset='utf8')
    cursor = db.cursor()
    if request.method == 'POST':
        file = request.files['voice']
        file.save(secure_filename(file.filename))
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
        file = request.files['voice']
        file.save(secure_filename(file.filename))

        # print(body.read())
    return render_template('login.html')


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
