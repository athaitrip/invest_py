from agents import momentum_agent, volatility_agent

ASSETS = ["SPY","GLD","TLT","UUP"]

def score_asset(symbol):
    mom = momentum_agent(symbol)
    vol = volatility_agent(symbol)

    # Hedge fund style:
    # reward momentum
    # penalize high vol
    score = (mom * 100) - (vol * 50)
    return score

def compute_scores():
    results = {}
    for a in ASSETS:
        results[a] = score_asset(a)
    return results