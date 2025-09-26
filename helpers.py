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
            
def admin_required(func):

    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        if not "user_id" in session or session["user_id"]!=1:    #the first user of the db file is set as the admin
                print("user is",session["user_id"])
                return render_template("login.html")
        return func(*args,**kwargs)
    return wrapper
##########################################################################################
from get_stock_data import get_stock_data
from scipy.optimize import newton
from datetime import datetime, date
import math

def xirr(cashflows, dates):
    if len(cashflows) < 2:
        return None
    # Analytical for exactly 2 cashflows
    if len(cashflows) == 2:
        cost = -cashflows[0]
        value = cashflows[1]
        days = (dates[1] - dates[0]).days
        if days <= 0 or cost <= 0 or value < 0:
            return None
        year_frac = days / 365.25
        ratio = value / cost
        if ratio <= 0:
            return -1.0
        try:
            r = math.pow(ratio, 1.0 / year_frac) - 1.0
            if math.isnan(r) or math.isinf(r):
                return None
            return r
        except (ValueError, OverflowError):
            return None
    # Numerical for more cashflows
    else:
        def npv(r):
            total = 0.0
            for i, cf in enumerate(cashflows):
                days_diff = (dates[i] - dates[0]).days / 365.25
                total += cf / (1 + r) ** days_diff
            return total
        try:
            return newton(npv, x0=0.0)
        except RuntimeError:
            return None

def calc_xirr(tdata):
    result = {}
    current_date = date.today()
    # Group by symbol
    from collections import defaultdict
    groups = defaultdict(list)
    for row in tdata:
        symbol = row["symbol"]
        groups[symbol].append(row)
    
    for symbol, rows in groups.items():
        cashflows = []
        dates = []
        total_shares = 0
        valid = True
        for row in rows:
            price = row["price"]
            shares = row["shares"]
            date_str = row["date"]
            try:
                purchase_date = datetime.strptime(date_str, '%d-%m-%Y').date()
            except ValueError:
                valid = False
                break
            if purchase_date >= current_date or shares <= 0:
                valid = False
                break
            cost = price * shares
            cashflows.append(-cost)
            dates.append(purchase_date)
            total_shares += shares
        
        if not valid or total_shares <= 0:
            result[symbol] = None
            continue
        
        try:
            current_price = float(get_stock_data(symbol)["regularMarketPrice"]) #here
        except:
            result[symbol] = None
            continue
        
        current_value = current_price * total_shares
        cashflows.append(current_value)
        dates.append(current_date)
        
        # Sort by date (in case rows not ordered)
        sorted_pairs = sorted(zip(dates, cashflows))
        dates = [d for d, c in sorted_pairs]
        cashflows = [c for d, c in sorted_pairs]
        
        result[symbol] = xirr(cashflows, dates)
    #print(result)
    return result

def year_diff(date1: str, date2: str) -> float:
    # Parse the dates
    d1 = datetime.strptime(date1, "%d-%m-%Y")
    d2 = datetime.strptime(date2, "%d-%m-%Y")
    
    # Ensure d1 <= d2
    if d1 > d2:
        return 0
    
    # Difference in days
    diff_days = (d2 - d1).days
    
    # Convert to years (using average year length)
    diff_years = diff_days / 365.2425  
    
    return diff_years



if __name__ == "__main__":

    import sqlite3
    conn = sqlite3.connect("users.db",check_same_thread=False)

    # Make the fetchall() returns list of dict like row elements instead of list of tuples.
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor()

    cur.execute("SELECT symbol, AVG(price) as price, SUM(shares) AS shares, date FROM holdings WHERE user_id=? AND symbol=?",(5,"INFY"))
    tdata = cur.fetchall()

    xirr = calc_xirr(tdata)

    print(xirr)
