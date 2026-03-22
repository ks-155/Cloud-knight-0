"""
PriceRadar — Market Simulation Engine
Generates realistic competitor prices with demand signals, festival
multipliers, day-of-week effects, and 7-day price history.
"""

import random
import math
from datetime import datetime, timedelta, timezone

# ── Competitor Definitions ────────────────────────────────────────
COMPETITORS = [
    {"id": "amazon",   "name": "Amazon India",      "logo": "🛒", "reliability": 0.95},
    {"id": "flipkart", "name": "Flipkart",           "logo": "🔵", "reliability": 0.93},
    {"id": "croma",    "name": "Croma",              "logo": "🟢", "reliability": 0.88},
    {"id": "reliance", "name": "Reliance Digital",   "logo": "🔴", "reliability": 0.85},
    {"id": "vijay",    "name": "Vijay Sales",        "logo": "🟠", "reliability": 0.82},
]

# ── Festival Calendar (month, day, name, demand_boost) ───────────
FESTIVALS = [
    (10, 20, "Diwali",         0.18),
    (10,  2, "Gandhi Jayanti", 0.05),
    ( 8, 15, "Independence Day", 0.08),
    ( 1, 26, "Republic Day",   0.07),
    ( 1,  1, "New Year",       0.10),
    (12, 25, "Christmas",      0.09),
    ( 6, 21, "Mid-Year Sale",  0.12),
]

# Variance per competitor (how much they deviate from market midpoint)
COMPETITOR_VARIANCE = {
    "amazon":   0.04,   # Very competitive — tight prices
    "flipkart": 0.05,
    "croma":    0.09,   # Slightly higher (brick-and-mortar overhead)
    "reliance": 0.08,
    "vijay":    0.10,   # Most variable
}


def _seeded_rand(product_id: str, competitor_id: str, day_offset: int = 0) -> random.Random:
    """Create a deterministic random generator so prices don't change on every request."""
    seed = hash(f"{product_id}-{competitor_id}-{day_offset}") & 0xFFFFFFFF
    return random.Random(seed)


def _festival_multiplier(dt: datetime = None) -> tuple[float, str | None]:
    """Return (multiplier, festival_name) for the given datetime."""
    if dt is None:
        dt = datetime.now(timezone.utc)

    for month, day, name, boost in FESTIVALS:
        # Within 7 days before the festival
        festival_date = dt.replace(month=month, day=day, hour=0, minute=0, second=0)
        diff = (festival_date - dt).days
        if 0 <= diff <= 7:
            # Boost ramps up as festival approaches
            proximity_factor = (8 - diff) / 8
            return 1 + (boost * proximity_factor), name
        # Day-of and day-after
        if -1 <= diff <= 0:
            return 1 + boost * 0.5, name

    return 1.0, None


def _day_of_week_multiplier(dt: datetime = None) -> float:
    """Weekend demand is higher for big-ticket items."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    # 0=Monday ... 6=Sunday
    dow = dt.weekday()
    if dow in (5, 6):   # Weekend
        return 1.04
    if dow == 4:        # Friday
        return 1.02
    return 1.0


def get_demand_signals(dt: datetime = None) -> dict:
    """Return current demand signals that affect pricing."""
    if dt is None:
        dt = datetime.now(timezone.utc)

    fest_mult, fest_name = _festival_multiplier(dt)
    dow_mult = _day_of_week_multiplier(dt)
    combined = fest_mult * dow_mult

    signals = {
        "overall_demand": round(combined, 3),
        "festival": fest_name,
        "festival_boost_pct": round((fest_mult - 1) * 100, 1),
        "weekend_boost_pct": round((dow_mult - 1) * 100, 1),
        "day_of_week": dt.strftime("%A"),
        "is_high_demand": combined > 1.08,
    }
    return signals


def get_competitor_prices(product: dict, your_price: float = None, dt: datetime = None) -> dict:
    """
    Generate a realistic set of competitor prices for a product.
    Returns prices, stats, market signals, and position analysis.
    """
    if dt is None:
        dt = datetime.now(timezone.utc)

    base = product["base_price"]
    product_id = product["id"]
    fest_mult, fest_name = _festival_multiplier(dt)
    dow_mult = _day_of_week_multiplier(dt)
    market_base = base * fest_mult * dow_mult

    prices = []
    for comp in COMPETITORS:
        rng = _seeded_rand(product_id, comp["id"])
        variance = COMPETITOR_VARIANCE[comp["id"]]
        # Skew: some competitors are usually cheaper/pricier
        skew = {"amazon": -0.02, "flipkart": -0.015, "croma": 0.03, "reliance": 0.02, "vijay": 0.04}
        factor = 1 + skew[comp["id"]] + rng.uniform(-variance, variance)
        price = round(market_base * factor, -1)  # Round to nearest 10

        prices.append({
            "competitor_id": comp["id"],
            "competitor_name": comp["name"],
            "logo": comp["logo"],
            "price": price,
            "in_stock": rng.random() > 0.08,   # 92% in-stock probability
            "delivery_days": rng.randint(1, 4),
            "rating": round(3.5 + rng.random() * 1.5, 1),
        })

    # Sort by price ascending
    prices.sort(key=lambda x: x["price"])

    # Stats
    price_values = [p["price"] for p in prices]
    avg = round(sum(price_values) / len(price_values), -1)
    lowest = min(price_values)
    highest = max(price_values)
    median = sorted(price_values)[len(price_values) // 2]

    # Tag cheapest / most expensive
    for p in prices:
        if p["price"] == lowest:
            p["tag"] = "cheapest"
        elif p["price"] == highest:
            p["tag"] = "priciest"
        else:
            p["tag"] = "mid"

    result = {
        "product_id": product_id,
        "competitors": prices,
        "market_stats": {
            "average": avg,
            "lowest": lowest,
            "highest": highest,
            "median": median,
            "spread_pct": round(((highest - lowest) / lowest) * 100, 1),
        },
        "demand_signals": get_demand_signals(dt),
    }

    if your_price is not None:
        gap = your_price - avg
        gap_pct = round((gap / avg) * 100, 1)
        result["your_position"] = {
            "your_price": your_price,
            "vs_average": round(gap, -1),
            "vs_average_pct": gap_pct,
            "vs_cheapest": round(your_price - lowest, -1),
            "position": (
                "below_market" if gap_pct < -5
                else "above_market" if gap_pct > 5
                else "at_market"
            ),
        }

    return result


def get_price_history(product: dict, days: int = 7) -> list[dict]:
    """
    Generate a realistic 7-day price history for each competitor.
    Returns list of daily data points with competitor breakdown.
    """
    now = datetime.now(timezone.utc)
    history = []

    for day_offset in range(days - 1, -1, -1):
        dt = now - timedelta(days=day_offset)
        base = product["base_price"]
        fest_mult, _ = _festival_multiplier(dt)
        dow_mult = _day_of_week_multiplier(dt)
        market_base = base * fest_mult * dow_mult

        daily_prices = {}
        for comp in COMPETITORS:
            rng = _seeded_rand(product["id"], comp["id"], day_offset)
            variance = COMPETITOR_VARIANCE[comp["id"]]
            skew = {"amazon": -0.02, "flipkart": -0.015, "croma": 0.03, "reliance": 0.02, "vijay": 0.04}
            factor = 1 + skew[comp["id"]] + rng.uniform(-variance, variance)
            daily_prices[comp["id"]] = round(market_base * factor, -1)

        avg = round(sum(daily_prices.values()) / len(daily_prices), -1)

        history.append({
            "date": dt.strftime("%Y-%m-%d"),
            "label": dt.strftime("%b %d"),
            "prices": daily_prices,
            "market_avg": avg,
        })

    return history
