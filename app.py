from fastapi import FastAPI
import requests
import os
import math

app = FastAPI()

# ---------- Config ----------
SYMBOLS = {
    "SPY": "stock",
    "GLD": "gold"
}

# ---------- Helper ----------
def fetch_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    r = requests.get(url, timeout=10)
    data = r.json()
    return data["quoteResponse"]["result"][0]["regularMarketPrice"]

def score_asset(symbol):
    try:
        price = fetch_price(symbol)
        score = math.log(price) % 100
        return round(score, 2)
    except:
        return 50

# ---------- API ----------
@app.get("/")
def home():
    return {"status": "Hedge Fund AI Agent Running"}

@app.get("/score")
def get_scores():
    results = {}
    for s in SYMBOLS:
        results[s] = score_asset(s)
    return results

@app.get("/allocation")
def allocation():
    scores = get_scores()
    total = sum(scores.values())
    alloc = {k: round(v/total, 2) for k,v in scores.items()}
    return alloc