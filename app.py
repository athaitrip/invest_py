from fastapi import FastAPI
from scoring import compute_scores
from portfolio import risk_parity_allocation

app = FastAPI()

@app.get("/")
def home():
    return {"status":"Hedge Fund AI Live"}

@app.get("/scores")
def scores():
    return compute_scores()

@app.get("/allocation")
def allocation():
    return risk_parity_allocation()