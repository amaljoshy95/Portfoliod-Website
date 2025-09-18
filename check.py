
import requests

"""
symbol = "INFY"
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=BG9Y53EILB7E9MKK'
r = requests.get(url,verify=False)
data = r.json()


url = "https://stock.indianapi.in/historical_data"

querystring = {"stock_name":"INFY","period":"1m","filter":"default"}

headers = {"X-Api-Key": "sk-live-uD5HFEfm4EbjlTYA58p3z4481mwRqBdxtPnEaifV"}

response = requests.get(url, headers=headers, params=querystring, verify=False)

"""
import yfinance as yf

# NSE tickers usually end with ".NS"
ticker = "RELIANCE.NS"  

# Download historical daily (EOD) data
data = yf.download(ticker, start="2025-01-01", end="2025-09-17", interval="1d")

print(data.head())