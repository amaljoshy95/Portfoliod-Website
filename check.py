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

mutual_fund_data()
