from flask import Flask,send_file,render_template,redirect,request,session
from werkzeug.security import generate_password_hash,check_password_hash
from dotenv import load_dotenv
from os import getenv
from helpers import login_required

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
    app.run(debug=True)

