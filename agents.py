from data import fetch_prices
import statistics

def momentum_agent(symbol):
    prices = fetch_prices(symbol)
    if len(prices) < 20:
        return 0
    return (prices[-1] / prices[-20] - 1)

def volatility_agent(symbol):
    prices = fetch_prices(symbol)
    if len(prices) < 20:
        return 0.5
    returns = [(prices[i]/prices[i-1]-1) for i in range(1,len(prices))]
    return statistics.stdev(returns)
