def momentum_agent(symbol):
    prices = fetch_prices(symbol)
    if len(prices) < 90:
        return 0
    return (prices[-1] / prices[-90] - 1)