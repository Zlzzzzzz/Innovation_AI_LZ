
import pandas as pd

def score_wallet(row):
    score = 50
    reasons = []

    if row["wallet_age_days"] >= 365:
        score += 15
        reasons.append("older wallet (+15)")
    elif row["wallet_age_days"] >= 90:
        score += 8
        reasons.append("moderately aged wallet (+8)")
    elif row["wallet_age_days"] < 30:
        score -= 12
        reasons.append("very new wallet (-12)")

    if row["active_days"] >= 30:
        score += 10
        reasons.append("activity spread across many days (+10)")
    elif row["active_days"] < 3:
        score -= 10
        reasons.append("very few active days (-10)")

    if row["tx_frequency"] > 5:
        score -= 15
        reasons.append("extremely high tx frequency (-15)")
    elif row["tx_frequency"] > 1:
        score -= 5
        reasons.append("high tx frequency (-5)")
    elif 0.01 <= row["tx_frequency"] <= 1:
        score += 5
        reasons.append("reasonable tx frequency (+5)")

    if row["burst_tx_ratio"] > 0.50:
        score -= 20
        reasons.append("very bursty behavior (-20)")
    elif row["burst_tx_ratio"] > 0.20:
        score -= 10
        reasons.append("moderately bursty behavior (-10)")
    else:
        score += 5
        reasons.append("low burst behavior (+5)")

    if row["unique_counterparties"] >= 10:
        score += 10
        reasons.append("high counterparty diversity (+10)")
    elif row["unique_counterparties"] <= 2:
        score -= 10
        reasons.append("very low counterparty diversity (-10)")

    if row["interaction_entropy"] >= 2:
        score += 8
        reasons.append("diverse interaction distribution (+8)")
    elif row["interaction_entropy"] < 0.5:
        score -= 8
        reasons.append("concentrated interaction pattern (-8)")

    if row["mean_time_gap_hours"] > 0 and row["mean_time_gap_hours"] < 0.1:
        score -= 10
        reasons.append("extremely short average time gaps (-10)")
    elif row["mean_time_gap_hours"] >= 1:
        score += 5
        reasons.append("reasonable average time gaps (+5)")

    if row["std_time_gap_hours"] == 0:
        score -= 5
        reasons.append("no timing variation (-5)")
    elif row["std_time_gap_hours"] > 1:
        score += 3
        reasons.append("natural timing variation (+3)")

    if "unique_token_symbols" in row.index:
        if row["unique_token_symbols"] >= 5:
            score += 5
            reasons.append("multiple token interactions (+5)")
        elif row["unique_token_symbols"] == 0:
            score -= 2
            reasons.append("no token diversity (-2)")

    score = max(0, min(100, score))

    return pd.Series({
        "human_score": score,
        "score_reasons": "; ".join(reasons)
    })


def human_likelihood(score):
    if score >= 75:
        return "High"
    elif score >= 50:
        return "Medium"
    return "Low"


def trust_tier(score):
    if score >= 80:
        return "Gold"
    elif score >= 60:
        return "Silver"
    return "Bronze"


def main():
    features = pd.read_csv("data/feature_table.csv")

    scored = features.copy()
    scored[["human_score", "score_reasons"]] = scored.apply(score_wallet, axis=1)

    scored["human_likelihood"] = scored["human_score"].apply(human_likelihood)
    scored["trust_tier"] = scored["human_score"].apply(trust_tier)

    output_cols = [
        "wallet",
        "human_score",
        "human_likelihood",
        "trust_tier",
        "score_reasons"
    ]

    scored[output_cols].to_csv("data/scoring_output.csv", index=False)

    print("Saved: data/scoring_output.csv")
    print(scored[output_cols].head())


if __name__ == "__main__":
    main()
