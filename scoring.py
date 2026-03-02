from agents import momentum_agent, volatility_agent

ASSETS = ["SPY","GLD","TLT","UUP"]

def score_asset(symbol):
    mom = momentum_agent(symbol)
    vol = volatility_agent(symbol)

    if vol == 0:
        vol = 0.0001

    # Risk adjusted return (Sharpe proxy)
    score = mom / vol
    return score

def compute_scores():
    results = {}
    for a in ASSETS:
        results[a] = score_asset(a)
    return results