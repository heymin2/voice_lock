from flask import Flask, render_template, redirect, request, url_for
import pymysql
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def voice():
    # jsonbody = request.get_json(force=True, silent=True)
    # name = jsonbody['name']
    # print(name)
    print(request.is_json)

    return render_template('voiceRecord.html')


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    db = pymysql.connect(host='localhost', port=3306, user='hyemin',
                         password='1234', db='user', charset='utf8')
    cursor = db.cursor()
    if request.method == 'POST':
        id = request.form.get('id')
        passwd = request.form.get('passwd')
        voice = "no"
        sql = "INSERT INTO user (id, pass, voice) VALUES (%s, %s, %s)"
        cursor.execute(sql, (id, passwd, voice))
        db.commit()
        return redirect(url_for('login'))
    return render_template('sign.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
