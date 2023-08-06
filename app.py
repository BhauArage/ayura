from ImageFinder import get_images_links as find_image
from base64 import encodebytes
from PIL import Image
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, abort,make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
import pandas as pd
# import pdfkit
import numpy as np
import model as m
import os

# imports
from flask import Flask, render_template, request
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer

import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

dataset = pd.read_csv('indian_food.csv')

app.secret_key = "ayura"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ayura"

mysql = MySQL(app)


@app.errorhandler(404)
def improper_access(error):
    # session.clear()
    # return jsonify(str(error))
    return render_template('error.html'), 404


@app.route("/")
@app.route("/index")
def index():
    # session["loggedin"] = False
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT users.*,test_result.dosh_identified FROM users LEFT JOIN test_result ON users.uid=test_result.uid WHERE email = % s AND password = % s", (username, password, ))
        # print("heyooooooo")
        account = cursor.fetchone()
        if account:
            session["loggedin"] = True
            session["uid"] = account["uid"]
            session["username"] = account["username"]
            session["email"] = account["email"]
            session["age"] = account["age"]
            session["dosh_identified"] = account["dosh_identified"]
            msg = "Logged in successfully !"
            # print(account)
            # print(session)
            return redirect(url_for('home'))
        else:
            msg = "Incorrect username / password !"
    return render_template("login.html", msg=msg)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        age = request.form["age"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        account = cursor.fetchone()
        if account:
            msg = "Account already exists !"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address !"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers !"
        else:
            cursor.execute("INSERT INTO users VALUES (NULL, % s, % s, % s, % s)",
                           (username, password, email, age, ))
            cursor.execute(
                "SELECT users.*,test_result.dosh_identified FROM users LEFT JOIN test_result ON users.uid=test_result.uid WHERE email = %s ORDER BY test_result.test_date DESC", (email, ))
            account = cursor.fetchone()
            # print(account)
            # print(session)
            if account:
                session["loggedin"] = True
                session["uid"] = account["uid"]
                session["username"] = account["username"]
                session["email"] = account["email"]
                session["age"] = account["age"]
                session["dosh_identified"] = account["dosh_identified"]
                # msg = "You have successfully registered !"
                # cursor.execute(
                #     "INSERT INTO test_result (uid) VALUES (%s)", (session["uid"],))
            mysql.connection.commit()
            return redirect(url_for('home'))
    return render_template("register.html", msg=msg)


def isLogged():
    try:
        if session["loggedin"]:
            return True
    except:
        return False
    # return False


@app.route("/profile")
def profile():
    if not isLogged():
        abort(404)
    return render_template("profile.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/home", methods=["POST", "GET"])
def home():
    if not isLogged():
        abort(404)
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        foodItem = request.form["tags"]
        cursor.execute(
            "INSERT INTO food_data (uid,food) VALUES (%s,%s)", (session["uid"], foodItem, ))
        mysql.connection.commit()
        msg = 'Inserted'
    cursor.execute(
        "SELECT food FROM food_data where date(date_added)=curdate() and uid=%s", (session["uid"], ))
    foodData = cursor.fetchall()
    return render_template("home.html", data=dataset['name'], msg=msg, foodData=foodData)


@app.route("/processdosha/<string:datamoved>", methods=["POST","GET"])
def processdosha(datamoved):
    datamoved = json.loads(datamoved)
    session["dosh_identified"] = datamoved['dosh']
    print(session)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO test_result (uid,dosh_identified,vata,pitta,kapha) VALUES (%s,%s,%s,%s,%s)",
                   (session["uid"], datamoved['dosh'], datamoved['vata'], datamoved['pitta'], datamoved['kapha'], ))
    mysql.connection.commit()
    return ("/")

## session is getting deleted.... yyyyyyyy

@app.route("/form", methods=["POST", "GET"])
def form():
    if not isLogged():
        abort(404)
    return render_template("form.html")


@app.route("/foodcorner", methods=["POST", "GET"])
def foodcorner():
    # try catch block here
    
    if not isLogged():
        abort(404)
    args = {}
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT food FROM food_data WHERE uid=%s ORDER BY date_added DESC", (session["uid"], ))
        # print(cursor.fetchone()['food'])
        title = cursor.fetchone()['food']
    except TypeError:
        title = dataset.sample()['name'].to_string(index=False)
    args['title'] = title
    try:
        cursor.execute(
            "SELECT dosh_identified FROM test_result WHERE uid=%s", (session["uid"], ))
        dosh = cursor.fetchone()['dosh_identified']
    except TypeError:
        dosh=''
    args['dosh'] = dosh
    Fooddata = m.get_recommendations(**args)
    FoodImage = [find_image(i) for i in Fooddata]
    Data = np.array((Fooddata, FoodImage)).T
    return render_template("foodcorner.html", data=Data)


def createGraph(percentageDosha, majorDosh, testdate):
    fig = plt.figure(figsize=(10, 7))
    plt.pie(percentageDosha, labels=['vata', 'pitta', 'kapha'])
    plt.title("{0} :  {1}".format(testdate, majorDosh))
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    pil_img = Image.open(img)
    pil_img.save(img, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(img.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img


def createBarGraph(dishes,counts):
    fig = plt.figure(figsize=(10, 5))
    plt.bar(dishes,counts)
    # plt.pie(percentageDosha, labels=['vata', 'pitta', 'kapha'])
    plt.title("Dishes and their count")
    plt.xlabel("Dishes")
    plt.ylabel("Count")
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    pil_img = Image.open(img)
    pil_img.save(img, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(img.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img


@app.route("/report", methods=["POST", "GET"])
def report():
    if not isLogged():
        abort(404)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM `test_result` t1 INNER Join `test_result` t2 ON t1.uid=t2.uid where DATEDIFF(t1.test_date,t2.test_date)>=14 and t1.uid=%s limit 4", (session["uid"], ))
    ReportData = cursor.fetchall()
    images = []
    afterimages = []
    food=[]
    barimages=[]
    for i in ReportData:
        img = createGraph(np.array(
            [i['vata'], i['pitta'], i['kapha']]), i['dosh_identified'], i['test_date'])
        afterimages.append(img)
        cursor.execute("SELECT distinct(food),count(food) FROM food_data where date(date_added) BETWEEN DATE(%s) AND DATE(%s) and uid=%s group by food", (i['t2.test_date'],i['test_date'],session["uid"], ))
        fooddata=cursor.fetchall()
        dishes=[]
        counts=[]
        for j in fooddata:
            dishes.append(j['food'])
            counts.append(j['count(food)'])
        barimg=createBarGraph(dishes,counts)
        barimages.append(barimg)
        # print(type(fooddata))
        food.append(fooddata)
        img = createGraph(np.array(
            [i['t2.vata'], i['t2.pitta'], i['t2.kapha']]), i['t2.dosh_identified'], i['t2.test_date'])
        images.append(img)
    # rendered=render_template("reports.html", images=zip(images, afterimages,food,barimages))
    # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    # pdf=pdfkit.from_string(rendered,configuration=config)
    # response=make_response(pdf)
    # response.headers['Content-Type']='application/pdf'
    # response.headers['Content-Dispostion']='inline; filename=output.pdf'
    # # return response
    return render_template("reports.html", images=zip(images, afterimages,food,barimages))

# @app.route("/download", methods=["POST", "GET"])
# def download():
    

if __name__ == "__main__":
    app.run(debug=True)
