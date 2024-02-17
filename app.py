from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import yaml

app = Flask(__name__)
app.secret_key='Bhavik'
#config db

db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST']= db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']= db['mysql_db']

mysql= MySQL(app)


@app.route('/index', methods={'GET', 'POST'})
def index():
    return render_template('index.html')

@app.route('/insert', methods={'GET', 'POST'})
def insert():
    return render_template('insert.html')

@app.route('/update', methods={'GET', 'POST'})
def update():
    return render_template('update.html')


# @app.route('/')
@app.route('/', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' :
        username = request.form['email']
        password = request.form['password']
        # return username,password
        u=username
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password))
        account = cursor.fetchone()
        if account:
            # session["loggedin"] = True
            # session["id"] = account["id"]
            # session["username"] = account["username"]
            msg = 'Logged in successfully !'
            # print(23456)
            return render_template('index.html', msg = msg,user=username)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/display', methods=['GET', 'POST'])
def display():
    #if request.method == "POST":
        #player_id = request.form['player_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from player")
        mysql.connection.commit()
        data=cur.fetchall()


        cur = mysql.connection.cursor()
        cur.execute("SELECT * from physical_details")
        mysql.connection.commit()
        data1 = cur.fetchall()
        #return render_template('display.html', data=data,data1=data1)


        cur = mysql.connection.cursor()
        cur.execute("SELECT * from player_history")
        mysql.connection.commit()
        data2 = cur.fetchall()
        #return render_template('display.html', data=data, data1=data1)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * from stats")
        mysql.connection.commit()
        data3 = cur.fetchall()
        #return render_template('display.html', data=data,data1=data1)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * from player_position")
        mysql.connection.commit()
        data4 = cur.fetchall()
        return render_template('display.html', data=data,data1=data1,data2=data2,data3=data3,data4=data4)
   # return render_template('display.html')

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        userDetails = request.form
        player_id = userDetails['player_id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM player WHERE player_id= % s ", (player_id))
        mysql.connection.commit()
        cur.close()
        flash('you are successfuly logged in')
    return render_template('delete.html')

@app.route('/supdate', methods=['GET','POST'])
def supdate():
    if request.method == 'POST':
        userDetails = request.form
        player_id = userDetails['player_id']
        running_speed = userDetails['running_speed']
        stamina = userDetails['stamina']
        strength = userDetails['strength']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE stats SET running_speed= %s, stamina=%s, strength=%s WHERE player_id= % s ", (running_speed, stamina, strength, player_id))
        mysql.connection.commit()
        cur.close()
    return render_template('supdate.html')

@app.route('/dupdate', methods=['GET','POST'])
def dupdate():
    if request.method == 'POST':
        userDetails = request.form
        player_id = userDetails['player_id']
        height = userDetails['height']
        weight = userDetails['weight']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE physical_details SET height= %s, weight=%s WHERE player_id= % s ", (height, weight, player_id))
        mysql.connection.commit()
        cur.close()
    return render_template('dupdate.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        player_id = request.form['player_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT player_id, sport from player where player_id LIKE %s OR sport LIKE %s",(player_id, player_id))
        mysql.connection.commit()
        data=cur.fetchall()
        if len(data) == 0 and player_id == 'all':
            cur.execute("SELECT * from player")
            mysql.connection.commit()
            data = cur.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')


#insert1
@app.route('/personal_details', methods=['GET','POST'])
def personal_details():
    if request.method == 'POST':
        userDetails = request.form
        player_id = userDetails['player_id']
        name = userDetails['name']
        age = userDetails['age']
        major = userDetails['major']
        sport = userDetails['sport']
    
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO player VALUES(%s,%s,%s,%s,%s)", (player_id, name, age, major, sport))
        mysql.connection.commit()
        cur.close()
    return render_template('personal_details.html')
#insert2
@app.route('/physical_details', methods=['GET','POST'])
def physical_details():
    if request.method == 'POST':
        userDetails = request.form
        player_id = userDetails['player_id']
        height = userDetails['height']
        weight = userDetails['weight']
        bmi=int(weight)/(int(height)*int(height))
        if bmi<18.5:
            status="Underweight"
        elif bmi>18.5 and bmi<24.9:
            status="Healthy Weight"
        elif 25<bmi<29.9:
            status="Over Weight"
        else:
            status="Obesity"
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO physical_details(player_id, height, weight,BMI,status) VALUES(%s,%s,%s,%s,%s)", (player_id, height, weight,bmi,status))
        mysql.connection.commit()
        cur.close()
    return render_template('physical_details.html')

#insert3

@app.route('/history', methods=['GET','POST'])
def history():
    if request.method == 'POST':
        userDetails = request.form
        player_id = userDetails['player_id']
        playing_since = userDetails['playing_since']
        level = userDetails['level']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO player_history VALUES(%s,%s,%s)", (player_id, playing_since, level))
        mysql.connection.commit()
        cur.close()
    return render_template('physical_details.html')
#insert4
@app.route('/position', methods=['GET','POST'])
def position():
    if request.method == 'POST':
        userDetails = request.form
        player_id = userDetails['player_id']
        sport = userDetails['sport']
        position = userDetails['position']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO player_position VALUES(%s,%s,%s)", (player_id, sport, position))
        mysql.connection.commit()
        cur.close()
    return render_template('physical_details.html')


#insert5
@app.route('/stats', methods=['GET','POST'])
def stats():
    if request.method == 'POST':
        userDetails = request.form
        player_id = userDetails['player_id']
        running_speed = userDetails['running_speed']
        stamina = userDetails['stamina']
        strength = userDetails['strength']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stats VALUES(%s,%s,%s)", (player_id, running_speed, stamina, strength))
        mysql.connection.commit()
        cur.close()
    return render_template('physical_details.html')


app.run(debug=True)

