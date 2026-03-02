import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

############################
# SAFE DATA FETCH (STOOQ)
############################

def get_stooq(symbol):
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=m"
    df = pd.read_csv(url)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    return df.sort_index()

def load_assets():
    symbols = {
        "SPY":"spy.us",
        "QQQ":"qqq.us",
        "GLD":"gld.us",
        "TLT":"tlt.us",
        "DBC":"dbc.us"
    }
    data = {}
    for k,v in symbols.items():
        data[k] = get_stooq(v)["Close"]
    return pd.DataFrame(data).dropna()

############################
# MODEL CORE
############################

def normalize(x):
    return np.tanh(x)

def growth_score(df):
    return normalize(df["SPY"].pct_change(6).iloc[-1]*3)

def inflation_score(df):
    return normalize(df["DBC"].pct_change(6).iloc[-1]*3)

def detect_regime(g,i):
    if g>0 and i<0: return "Goldilocks"
    if g>0 and i>0: return "Overheat"
    if g<0 and i<0: return "Recession"
    return "Stagflation"

def risk_parity(df):
    returns = df.pct_change().dropna()
    vol = returns.std()
    inv = 1/vol
    return inv/inv.sum()

def aggressive_tilt(w, regime):
    tilt = {
        "Goldilocks":{"SPY":1.4,"QQQ":1.5},
        "Overheat":{"GLD":1.5,"DBC":1.4},
        "Recession":{"TLT":1.5},
        "Stagflation":{"GLD":1.6,"DBC":1.5}
    }
    if regime in tilt:
        for k,f in tilt[regime].items():
            if k in w: w[k]*=f
    return w/w.sum()

def momentum_overlay(df,w):
    for a in w.index:
        mom = df[a].pct_change(6).iloc[-1]
        if mom<0: w[a]*=0.5
        elif mom>0.1: w[a]*=1.1
    return w/w.sum()

############################
# DASHBOARD
############################

@app.get("/", response_class=HTMLResponse)
def dashboard():

    df = load_assets()
    returns = df.pct_change().dropna()

    g = growth_score(df)
    i = inflation_score(df)
    regime = detect_regime(g,i)

    w = risk_parity(df)
    w = aggressive_tilt(w, regime)
    w = momentum_overlay(df,w)

    port = (returns*w).sum(axis=1)
    cum = (1+port).cumprod()

    cagr = cum.iloc[-1]**(12/len(cum))-1
    sharpe = port.mean()/port.std()*np.sqrt(12)
    maxdd = (cum/cum.cummax()-1).min()

    return f"""
    <html>
    <head>
    <title>AI Macro Portfolio</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
    body {{background:#0f172a;color:white;font-family:Arial;padding:20px}}
    .card {{background:#1e293b;padding:20px;border-radius:15px;margin:10px}}
    .grid {{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px}}
    h1 {{color:#38bdf8}}
    .badge {{padding:8px 15px;border-radius:20px;background:#22c55e}}
    </style>
    </head>
    <body>

    <h1>AI Dalio Aggressive Portfolio</h1>
    <div class="badge">Regime: {regime}</div>

    <div class="grid">
        <div class="card"><h3>CAGR</h3><h2>{round(cagr*100,2)}%</h2></div>
        <div class="card"><h3>Sharpe</h3><h2>{round(sharpe,2)}</h2></div>
        <div class="card"><h3>Max DD</h3><h2>{round(maxdd*100,2)}%</h2></div>
    </div>

    <div class="card"><canvas id="pie"></canvas></div>
    <div class="card"><canvas id="line"></canvas></div>

    <script>
    const weights = {w.round(3).to_dict()};
    new Chart(document.getElementById('pie'), {{
        type:'pie',
        data:{{labels:Object.keys(weights),
        datasets:[{{data:Object.values(weights)}}]}}
    }});

    new Chart(document.getElementById('line'), {{
        type:'line',
        data:{{labels:{list(cum.index.strftime("%Y-%m"))},
        datasets:[{{data:{list(cum.round(3))},
        borderColor:'#38bdf8'}}]}}
    }});
    </script>

    </body>
    </html>
    """