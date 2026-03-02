from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scoring import compute_scores
from portfolio import risk_parity_allocation

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"status": "All Weather AI Running"}

@app.get("/scores")
def scores():
    return compute_scores()

@app.get("/allocation")
def allocation():
    return risk_parity_allocation()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    scores = compute_scores()
    allocation = risk_parity_allocation()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "scores": scores,
        "allocation": allocation
    })