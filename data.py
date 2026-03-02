def fetch_prices(symbol):
    try:
        r = requests.get(YF_URL.format(symbol), timeout=10)
        data = r.json()
        closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        return [c for c in closes if c]
    except:
        return []