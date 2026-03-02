from scoring import compute_scores

def risk_parity_allocation():
    scores = compute_scores()
    positive = {k:v for k,v in scores.items() if v > 0}

    if not positive:
        return {"CASH":1.0}

    total = sum(positive.values())
    alloc = {k: round(v/total,2) for k,v in positive.items()}
    return alloc