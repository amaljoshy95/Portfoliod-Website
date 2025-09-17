from flask import Flask,send_file,render_template,redirect,request,session,url_for,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from dotenv import load_dotenv
from os import getenv
from helpers import login_required,get_stock_data

load_dotenv()
Flask.secret_key = getenv("FLASK_SECRET_KEY")

app = Flask(__name__)

import sqlite3
conn = sqlite3.connect("users.db",check_same_thread=False)

# Make the fetchall() returns list of dict like row elements instead of list of tuples.
conn.row_factory = sqlite3.Row 
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY NOT NULL, username TEXT NOT NULL, 
                hash TEXT NOT NULL)""")
conn.commit()



@app.route("/")
@login_required
def index():
    
    return render_template("index.html")


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
    
    symbol = request.form.get("stockSymbol")
    price = request.form.get("price")

    if not symbol:
        return redirect(url_for("buy",error="Enter a symbol!"))

    response = get_stock_data(symbol)
    if response["status"]=="error":
        return redirect(url_for("buy",error="Invalid Symbol!"))

    current_price = response["values"][0]["close"]
    if not price:

        return redirect(url_for("buy",valid='true',current_price=current_price))

    try:
        price = int(price)
    except:
        return redirect(url_for("buy",error="Enter a valid price!"))
    
    if price<=0:
        return redirect(url_for("buy",error="Enter a valid price!"))









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
    app.run(host="0.0.0.0",debug=True)

