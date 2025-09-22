import bse
from get_stock_data import get_stock_data

def bse_search(stock):
    
    stock = "HDFCBANK"
    b= bse.BSE(r"C:\Users\amaljoshykj\Downloads")
    bsecode = b.getScripCode("HDFCBANK")


import yfinance as yf
import os,certifi
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


def mutual_fund_data():
    fund = yf.Ticker("0P0000XW8F.BO")
    hist = fund.history(period="1y")
    print(hist)


import requests
def etmoneysearch():

    query = "pgim"
    url = f"https://www.moneycontrol.com/mccode/common/autosuggestion_solr.php?classic=false&query={query}&type=2&format=json&main=false"
    ""

    payload = {"query": "pgim",
               
               }   # replace with stock name you want to search
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"  # some APIs require a UA
    }

    response = requests.get(url, headers=headers)

    # Raise error if request failed
    response.raise_for_status()

    # Response is usually JSON
    data = response.json()
    data = [k["name"] for k in data]
    print(data)

etmoneysearch()        
