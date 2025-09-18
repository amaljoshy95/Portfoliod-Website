from flask import Flask,send_file,render_template,redirect,request,session,url_for,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from dotenv import load_dotenv
from os import getenv
from helpers import login_required,get_stock_data
from datetime import date
from get_stock_data import get_stock_data

load_dotenv()
Flask.secret_key = getenv("FLASK_SECRET_KEY")

app = Flask(__name__)

import sqlite3
conn = sqlite3.connect("users.db",check_same_thread=False)

# Make the fetchall() returns list of dict like row elements instead of list of tuples.
conn.row_factory = sqlite3.Row 
cur = conn.cursor()

# enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON")

cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY NOT NULL, username TEXT NOT NULL, 
                hash TEXT NOT NULL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS holdings (id INTEGER PRIMARY KEY NOT NULL, symbol TEXT NOT NULL,
            shares NUMBER NOT NULL, price FLOAT NOT NULL, date TEXT NOT NULL, user_id INTEGER NOT NULL, 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)""")
conn.commit()




@app.route("/")
@login_required
def index():
    
    user_id = session["user_id"]
    cur.execute("""SELECT symbol, SUM(price*shares)*1.0/SUM(shares) AS price, SUM(shares) AS shares, date 
                FROM holdings WHERE user_id = ? GROUP BY symbol""",(user_id,))
    hdata = cur.fetchall()
    
    return render_template("index.html",hdata=hdata, get_stock_data=get_stock_data)



@app.route("/stock_detail_api/<symbol>")
@login_required
def stock_detail_api(symbol):

    response = get_stock_data(symbol)

    return jsonify(response)



@app.route("/buy",methods=["GET","POST"])
@login_required
def buy():

    if request.method=="GET":
        return render_template("buy.html")
    
    data = request.get_json()

    symbol = data.get("symbol")
    price = data.get("buyPrice")
    shares = data.get("shares")

    if not symbol or not price or not shares:
        return "",400
    
    try:
        price = float(price)
        shares = int(shares)
        if price<0 or shares<0:
            return "",400
    except:
        return "",400
    
    user_id = session["user_id"]
    curr_date = date.today().strftime("%d-%m-%Y")

    cur.execute("INSERT INTO holdings (symbol,shares,price,date,user_id) VALUES (?,?,?,?,?)",(symbol,shares,price,curr_date,user_id))
    conn.commit()

    return jsonify({}),200

    

@app.route("/login", methods=["POST","GET"])
def login():

    if request.method=="GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html",message="Please provide username and password!")

    cur.execute("SELECT id,hash FROM users WHERE username=? LIMIT 1",(username,))
    id_and_hash = cur.fetchall()

    if not id_and_hash:
        return render_template("login.html", message="Invalid Username!")
    
    hash = id_and_hash[0]["hash"]
    if check_password_hash(hash,password):

        session["user_id"] = id_and_hash[0]["id"]
        return redirect("/")
    
    return render_template("login.html",message="Invalid Password!")



@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    username = request.form.get("username")

    if not password or not confirm_password or not username:
        return render_template("signup.html",message="✖ Invalid username or password!")
    
    if password != confirm_password:
        return render_template("signup.html", message="✖ Passwords don't match!")


    cur.execute("SELECT id FROM users WHERE username=? LIMIT 1",(username,))
    id = cur.fetchall()

    if id:
        return render_template("signup.html", message="✖ Username already exists!")

    hash = generate_password_hash(password)

    cur.execute("INSERT INTO users (username,hash) VALUES (?,?)",(username,hash))
    conn.commit()

    cur.execute("SELECT id FROM users WHERE username=? LIMIT 1",(username,))
    id = cur.fetchall()[0]["id"]
    session["user_id"] = id

    return redirect("/")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

