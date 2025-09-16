import sqlite3
from flask import session,render_template
import functools


def login_required(func):
    @functools.wraps(func)
    def wrapper():
        if not "user_id" in session:
                return render_template("login.html")
        return_file = func()
        return return_file
    return wrapper
            
            


