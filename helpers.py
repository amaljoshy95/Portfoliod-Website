import sqlite3
from flask import session,render_template
import functools
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        if not "user_id" in session:
                return render_template("login.html")
        return func(*args,**kwargs)
    return wrapper
            

def get_stock_data(symbol):

    api_key = getenv("API_KEY_TWELVE_DATA")
    url = f"https://api.twelvedata.com/time_series?apikey={api_key}&interval=1day&country=India&exchange=NSE&symbol={symbol}&type=stock&outputsize=20&previous_close=true&format=JSON"

    response = requests.get(url=url, verify=False).json()
    return response

