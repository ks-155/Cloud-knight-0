"""
PriceRadar — ML Pricing Model
GradientBoostingRegressor trained on synthetic data to recommend
optimal retail prices based on competitive + demand signals.
"""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import random

# ── Training Data Generation ──────────────────────────────────────
def _generate_training_data(n_samples: int = 12000) -> tuple:
    """
    Generate synthetic (but realistic) training samples.

    Features:
        0. competitor_avg_price        — market average (₹)
        1. your_price_ratio            — your_price / competitor_avg
        2. price_spread_pct            — (highest - lowest) / lowest * 100
        3. demand_signal               — combined demand multiplier (1.0–1.25)
        4. day_of_week                 — 0 (Mon) to 6 (Sun)
        5. days_until_festival         — 0–30 (30 = no festival soon)
        6. category_elasticity         — 0.25–0.65
        7. competitor_count_below      — how many competitors are cheaper

    Target: optimal_price_ratio (optimal_price / competitor_avg)
    """
    rng = random.Random(42)
    np_rng = np.random.RandomState(42)

    X, y = [], []

    elasticity_values = [0.25, 0.45, 0.50, 0.55, 0.65]
    base_prices = [500, 2000, 8000, 30000, 75000, 130000]

    for _ in range(n_samples):
        base = rng.choice(base_prices)
        comp_avg = base * rng.uniform(0.90, 1.10)
        elasticity = rng.choice(elasticity_values)

        your_price_ratio = rng.uniform(0.80, 1.25)
        spread_pct = rng.uniform(3, 18)
        demand = rng.uniform(1.0, 1.20)
        dow = rng.randint(0, 6)
        days_festival = rng.randint(0, 30)
        comp_below_you = rng.randint(0, 5)

        # Business rule: optimal ratio balances margin vs. volume
        # Higher elasticity → recommend closer to market (or slightly below)
        # High demand → can price slightly higher
        # Many competitors below → should lower price
        base_ratio = 0.97 + (1 - elasticity) * 0.06
        demand_adj = (demand - 1.0) * 0.15
        festival_adj = max(0, (7 - days_festival) / 7) * 0.03 if days_festival < 7 else 0
        comp_adj = -comp_below_you * 0.008
        noise = np_rng.normal(0, 0.008)

        optimal_ratio = base_ratio + demand_adj + festival_adj + comp_adj + noise
        optimal_ratio = max(0.82, min(1.18, optimal_ratio))  # Clamp

        X.append([
            comp_avg,
            your_price_ratio,
            spread_pct,
            demand,
            dow,
            days_festival,
            elasticity,
            comp_below_you,
        ])
        y.append(optimal_ratio)

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


# ── Model Training (runs once at import time, ~1 second) ──────────
print("🤖 PriceRadar ML: Training pricing model...")
_X, _y = _generate_training_data(12000)
_scaler = StandardScaler()
_X_scaled = _scaler.fit_transform(_X)

_model = GradientBoostingRegressor(
    n_estimators=120,
    max_depth=5,
    learning_rate=0.08,
    subsample=0.85,
    random_state=42,
)
_model.fit(_X_scaled, _y)
print(f"✅ Model trained. Train R²: {_model.score(_X_scaled, _y):.3f}")


# ── Public API ────────────────────────────────────────────────────
def recommend_price(
    your_price: float,
    cost_price: float,
    competitor_avg: float,
    spread_pct: float,
    demand_signal: float,
    day_of_week: int,
    days_until_festival: int,
    category_elasticity: float,
    competitors_below_you: int,
) -> dict:
    """
    Returns an optimal price recommendation with supporting analytics.

    Returns:
        optimal_price        — recommended price (₹)
        expected_demand_chg  — projected change in buyer volume (%)
        confidence_score     — model confidence 0–100
        action               — 'reduce', 'increase', or 'hold'
        reason               — human-readable explanation
        margin_impact        — estimated margin change if suggestion followed
    """
    features = np.array([[
        competitor_avg,
        your_price / competitor_avg,
        spread_pct,
        demand_signal,
        day_of_week,
        days_until_festival,
        category_elasticity,
        competitors_below_you,
    ]], dtype=np.float32)

    features_scaled = _scaler.transform(features)
    optimal_ratio = float(_model.predict(features_scaled)[0])
    optimal_price = round(competitor_avg * optimal_ratio, -1)  # Round to 10

    floor_price = round(cost_price * 1.05, -1)
    is_clamped = optimal_price < floor_price
    if is_clamped:
        optimal_price = floor_price

    # Demand change: based on price elasticity and price change
    price_change_pct = (optimal_price - your_price) / your_price * 100
    demand_chg = -price_change_pct * category_elasticity   # Price down → demand up
    demand_chg = round(demand_chg, 1)

    # Confidence: inversely related to spread (tight market = more certain)
    confidence = max(55, min(96, int(88 - spread_pct * 0.8 + demand_signal * 5)))

    # Action
    gap_pct = (optimal_price - your_price) / your_price * 100
    if gap_pct < -2:
        action = "reduce"
    elif gap_pct > 2:
        action = "increase"
    else:
        action = "hold"

    # Reason
    reasons = []
    if is_clamped:
        reasons.append("Protected 5% minimum profit margin against aggressive competitor discounting")
    else:
        if competitors_below_you >= 3:
            reasons.append(f"{competitors_below_you} of 5 competitors are cheaper than you")
        if demand_signal > 1.08:
            reasons.append("market demand is elevated — buyers are active")
        if days_until_festival < 7 and days_until_festival >= 0:
            reasons.append(f"festival season approaching — demand boost expected")
        if day_of_week in (5, 6):
            reasons.append("weekend purchase intent is higher")
        if not reasons:
            reasons.append("market prices are closely clustered")

    margin_impact = round((optimal_price - cost_price) / cost_price * 100, 1) if cost_price > 0 else 0.0

    return {
        "optimal_price":       optimal_price,
        "expected_demand_chg": demand_chg,
        "confidence_score":    confidence,
        "action":              action,
        "gap_from_current_pct": round(gap_pct, 1),
        "reason":              "; ".join(reasons),
        "margin_impact_pct":   margin_impact,
    }
