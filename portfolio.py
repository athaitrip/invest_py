from scoring import compute_scores

TARGET_VOL = 0.12  # 12% annual target

def risk_parity_allocation():
    scores = compute_scores()

    positive = {k:v for k,v in scores.items() if v > 0}

    if not positive:
        return {"CASH":1.0}

    inv_vol_sum = sum(1/abs(v) for v in positive.values())

    weights = {}
    for k,v in positive.items():
        weights[k] = round((1/abs(v)) / inv_vol_sum,2)

    return weights