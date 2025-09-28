import requests
import json
from datetime import datetime

def get_stock_data(symbol, viewrange="1mo", interval="1d"):

    if symbol.endswith(".NS"):
        symbol = symbol.removesuffix(".NS")
    elif symbol.endswith(".BO"):
        symbol = symbol.removesuffix(".BO")

    symbol = symbol.strip()

    try:
        try:
            nse_symbol = symbol+".NS"
            base_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{nse_symbol}"
            params = {
                    "range": viewrange,
                    "interval": interval
                    }       
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(base_url, headers=headers, params=params)
            #print("Final url",response.url)
            response.raise_for_status()
            data = response.json()

        except:
            nse_symbol = symbol+".BO"
            base_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{nse_symbol}"
            params = {
                    "range": viewrange,
                    "interval": interval
                    }       
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(base_url, headers=headers, params=params)
            #print("Final url",response.url)
            response.raise_for_status()
            data = response.json()

    except:
        try:
            try:
                bse_symbol = symbol+".BO"
                url = f"https://query1.finance.yahoo.com/v7/finance/spark?includePrePost=true&includeTimestamps=true&indicators=close&interval={interval}&range={viewrange}&symbols={bse_symbol}&lang=en-US&region=US"
                #print(url)
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
            
            except:
                bse_symbol = symbol+".NS"
                url = f"https://query1.finance.yahoo.com/v7/finance/spark?includePrePost=true&includeTimestamps=true&indicators=close&interval={interval}&range={viewrange}&symbols={bse_symbol}&lang=en-US&region=US"
                #print(url)
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()

        except:
            
            
                #for global stocks
                url = f"https://query1.finance.yahoo.com/v7/finance/spark?includePrePost=true&includeTimestamps=true&indicators=close&interval={interval}&range={viewrange}&symbols={symbol}&lang=en-US&region=US"
                #print(url)
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
            
           
                

    # Extract the result object
    try:
        result = data["chart"]["result"][0]
        meta = result["meta"]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]
    except:
        result = data["spark"]["result"][0]["response"][0]
        meta = result["meta"]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]     

    # Format historical prices
    history = []
    for ts, close in zip(timestamps, closes):
        history.append({
            "date": datetime.fromtimestamp(ts).strftime("%Y-%m-%d"),
            "price": close
        })

    # Combine stock details + history
    final_json = {
        "symbol": meta.get("symbol"),
        "name": meta.get("longName"),
        "exchange": meta.get("exchangeName"),
        "currency": meta.get("currency"),
        "timezone": meta.get("timezone"),
        "regularMarketPrice": meta.get("regularMarketPrice"),
        "fiftyTwoWeekHigh": meta.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": meta.get("fiftyTwoWeekLow"),
        "history": history
    }

    return final_json


if __name__ == "__main__":
    stock_json = get_stock_data("INFY.NS", range="1mo", interval="1d")
    print(json.dumps(stock_json, indent=2))


"""
Example output:
{
  "symbol": "RELIANCE.NS",
  "name": "Reliance Industries Limited",
  "exchange": "NSI",
  "currency": "INR",
  "timezone": "IST",
  "regularMarketPrice": 1413.8,
  "fiftyTwoWeekHigh": 1551.0,
  "fiftyTwoWeekLow": 1114.85,
  "history": [
    {"date": "2025-08-23", "price": 1381.7},
    {"date": "2025-08-24", "price": 1420.1},
    {"date": "2025-08-25", "price": 1413.0}
  ]
}

"""