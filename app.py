import os
import csv
from flask import Flask, url_for, render_template, request, redirect, send_file, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import pymysql


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    return render_template('signIn.html')


@app.route('/sign-in-do', methods=['GET', 'POST'])
def sign_in_do():
    if request.method == 'POST':
        data = [request.form['username'], request.form['password']]
        conn = pymysql.connect(host='172.17.0.2', user='root',
                               password='0000', db='testdb')
        curs = conn.cursor()
        sql = 'select username,password from USER'
        curs.execute(sql)
        output = curs.fetchall()
        userinfo = []
        for i in range(len(output)):
            username = output[i][0]
            password = output[i][1]

            userinfo.append([username, password])
        try:
            if data in userinfo:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Retry'
        except:
            return 'retry'
    conn.close()


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    return render_template('signUp.html')


@app.route('/sign-up-do', methods=['GET', 'POST'])
def sign_up_do():
    if request.method == 'POST':
        data = [request.form['username'],
                request.form['password'], request.form['email']]
        conn = pymysql.connect(host='172.17.0.2', user='root',
                               password='0000', db='testdb')
        curs = conn.cursor()

        sql = 'select username from USER'
        curs.execute(sql)
        output = curs.fetchall()
        userinfo = []
        for i in range(len(output)):
            username = output[i][0]
            userinfo.append(username)

        if data[0] in userinfo:
            return 'already create'
        else:
            sql = 'insert into USER (username,password,email) value (%s, %s, %s)'
            curs.execute(sql, data)
            conn.commit()
        conn.close()
        return render_template('signIn.html')


@app.route("/sign-out")
def sign_out():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route('/non-labelled', methods=['GET', 'POST'])
def non_labelled():
    return render_template('nonLabelled.html')


@app.route('/image-up', methods=['GET', 'POST'])
def image_up():
    files = os.listdir("./uploaded_img")
    return render_template('imageUp.html', files=files)


@app.route('/image-up-do', methods=['GET', 'POST'])
def image_up_do():
    if request.method == 'POST':
        image = request.files['image']
        image.save('./uploaded_img/' + secure_filename(image.filename))
        return 'Image upload success!'
    else:
        return render_template('page_not_found.html')


@app.route('/image-down', methods=['GET', 'POST'])
def image_down():
    files = os.listdir("./uploaded_img")
    return render_template('imageDown.html', files=files)


@app.route('/image-down-do', methods=['GET', 'POST'])
def image_down_do():
    if request.method == 'POST':
        files = os.listdir("./uploaded_img")
        for file in files:
            if file == request.form['img']:
                return send_file("./uploaded_img/" + request.form['img'], attachment_filename=request.form['img'], as_attachment=True)

    else:
        return 'no search file...'


@app.route('/labelled', methods=['GET', 'POST'])
def labelled():
    return render_template('labelled.html')


@app.route('/csv-up', methods=['GET', 'POST'])
def csv_up():
    files = os.listdir("./uploaded_csv")
    return render_template('csvUp.html', files=files)


@app.route('/csv-up-do', methods=['GET', 'POST'])
def csv_up_do():
    if request.method == 'POST':
        csv = request.files['csv']
        csv.save('./uploaded_csv/' + secure_filename(csv.filename))
        return 'CSV upload success!'
    else:
        return render_template('page_not_found.html')


@app.route('/csv-down', methods=['GET', 'POST'])
def csv_down():
    files = os.listdir("./uploaded_csv")
    return render_template('csvDown.html', files=files)


@app.route('/csv-down-do', methods=['GET', 'POST'])
def csv_down_do():
    if request.method == 'POST':
        files = os.listdir("./uploaded_csv")
        for file in files:
            if file == request.form['csv']:
                return send_file("./uploaded_csv/" + request.form['csv'], attachment_filename=request.form['csv'], as_attachment=True)

    else:
        return 'no search file...'
    return ''


@app.route('/verified', methods=['GET', 'POST'])
def verified():
    return render_template('verified.html')


@app.route('/input-db', methods=['GET', 'POST'])
def input_db():
    files = os.listdir("./uploaded_csv")
    return render_template('inputDb.html', files=files)


@app.route('/input-db-do', methods=['GET', 'POST'])
def input_db_do():
    if request.method == 'POST':
        files = os.listdir("./uploaded_csv")
        for file in files:
            if file == request.form['csv']:
                filename = open(file, 'r')
                csvRead = csv.reader(filename)
                conn = pymysql.connect(
                    host='172.17.0.2', user='root', password='0000', db='testdb')
                curs = conn.cursor()
                for row in csvRead:
                    image_name = (row[0])
                    x_min = (row[1])
                    y_min = (row[2])
                    x_max = (row[3])
                    y_max = (row[4])
                    label = (row[5])
                    sql = "insert into DATA (image, xmin, ymin, xmax, ymax, label) value ( %s, %f, %f, %f, %f, %s)"
                    curs.execute(
                        sql, (image_name, x_min, x_max, y_min, y_min, label))

                    conn.commit()
                    filename.close()
                conn.close()

                return 'DB write success!!'
            else:
                return 'Failed...'


@app.route('/export', methods=['GET', 'POST'])
def export():
    conn = pymysql.connect(host='172.17.0.2', user='root',
                           password='0000', db='testdb')
    curs = conn.cursor()
    sql = 'select * from DATA'
    curs.execute(sql)
    output = curs.fetchall()
    conn.close()
    return render_template('export.html', output=output)


@app.route('/export-do', methods=['GET', 'POST'])
def export_do():
    if request.method == 'POST':
        conn = pymysql.connect(host='172.17.0.2', user='root',
                               password='0000', db='testdb')
        curs = conn.cursor()
        sql = 'select * from DATA'
        curs.execute(sql)
        output = curs.fetchall()
        file = open("dataset.csv", mode='w')
        writer = csv.writer(file)
        writer.writerow(["image", "xmin", "ymin", "xmax", "ymax", "label"])
        for item in output:
            writer.writerow(list(item.values()))
        conn.close()
        return redirect("/export")

    else:
        return render_template('retry')


if __name__ == '__main__':
    app.secret_key = "123123123"
    app.run(host='0.0.0.0', port=80, debug=True)
