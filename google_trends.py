"""
PriceRadar — Google Trends Wrapper
Uses pytrends to fetch real Google Trends data.
Falls back to realistic synthetic data if the API is rate-limited.
"""

import random
from datetime import datetime, timezone

# Try to import pytrends; gracefully fall back if unavailable
try:
    from pytrends.request import TrendReq
    _PYTRENDS_AVAILABLE = True
except ImportError:
    _PYTRENDS_AVAILABLE = False

_pytrends = None


def _get_client():
    global _pytrends
    if _pytrends is None and _PYTRENDS_AVAILABLE:
        _pytrends = TrendReq(hl="en-IN", tz=330)  # Indian locale, IST
    return _pytrends


def _synthetic_trend(keyword: str, timeframe: str = "today 7-d") -> dict:
    """
    Generate a realistic synthetic Google Trends response when the
    real API is not available or rate-limited.
    """
    rng = random.Random(hash(keyword.lower()) & 0xFFFF)
    base = rng.randint(30, 70)
    trend_up = rng.random() > 0.4   # 60% chance trending up

    # 7 daily points
    days = 7
    values = []
    cur = base
    for _ in range(days):
        delta = rng.randint(2, 12) * (1 if trend_up else -1)
        cur = max(5, min(100, cur + delta + rng.randint(-5, 5)))
        values.append(cur)

    # Related queries (hardcoded clusters)
    related_map = {
        "samsung":     ["samsung galaxy s24", "samsung tv 65 inch", "samsung fridge price", "samsung fold"],
        "iphone":      ["iphone 15 pro price", "iphone 15 price in india", "new iphone launch", "iphone 16"],
        "nike":        ["nike air max", "nike sale", "nike app india", "nike running shoes men"],
        "laptop":      ["best laptop under 50000", "gaming laptop india", "macbook air m3", "dell xps"],
        "headphones":  ["wireless headphones under 2000", "sony wh1000xm5", "noise cancelling earbuds"],
        "tv":          ["65 inch tv price", "4k tv under 80000", "oled tv india", "smart tv best brand"],
    }
    related = []
    for key, suggestions in related_map.items():
        if key in keyword.lower():
            related = suggestions[:5]
            break
    if not related:
        related = [f"{keyword} price", f"best {keyword}", f"{keyword} review", f"{keyword} buy online"]

    current_val = values[-1]
    peak_val    = max(values)
    breakout    = (current_val >= 70 and current_val >= peak_val * 0.9)

    return {
        "keyword": keyword,
        "timeframe": timeframe,
        "interest_over_time": values,
        "current_interest": current_val,
        "peak_interest": peak_val,
        "trend_direction": "rising" if values[-1] > values[0] else "falling",
        "breakout": breakout,
        "status": "Breakout 🚀" if breakout else ("Rising 📈" if values[-1] > values[0] else "Declining 📉"),
        "related_queries": related,
        "geo": "IN",
        "source": "synthetic",
    }


def get_google_trends(keyword: str, timeframe: str = "today 7-d") -> dict:
    """
    Fetch Google Trends interest over time.
    Returns real pytrends data if available, else synthetic fallback.
    """
    client = _get_client()

    if client:
        try:
            client.build_payload([keyword], timeframe=timeframe, geo="IN")
            df = client.interest_over_time()

            if df.empty:
                return _synthetic_trend(keyword, timeframe)

            values    = df[keyword].tolist()[-7:]   # Last 7 points
            dates     = [str(d)[:10] for d in df.index.tolist()][-7:]
            curr_val  = int(values[-1])
            peak_val  = int(max(values))
            breakout  = (curr_val >= 70 and curr_val >= peak_val * 0.9)

            # Related queries
            related_data = client.related_queries()
            rising = related_data.get(keyword, {}).get("rising")
            top    = related_data.get(keyword, {}).get("top")
            related = []
            if rising is not None and not rising.empty:
                related = rising["query"].tolist()[:5]
            elif top is not None and not top.empty:
                related = top["query"].tolist()[:5]

            return {
                "keyword":           keyword,
                "timeframe":         timeframe,
                "interest_over_time": values,
                "dates":             dates,
                "current_interest":  curr_val,
                "peak_interest":     peak_val,
                "trend_direction":   "rising" if values[-1] > values[0] else "falling",
                "breakout":          breakout,
                "status":            "Breakout 🚀" if breakout else ("Rising 📈" if values[-1] > values[0] else "Declining 📉"),
                "related_queries":   related,
                "geo":               "IN",
                "source":            "google_trends",
            }

        except Exception as e:
            # Rate limited or error — fall back gracefully
            result = _synthetic_trend(keyword, timeframe)
            result["error"] = f"pytrends fallback: {str(e)[:80]}"
            return result

    return _synthetic_trend(keyword, timeframe)


def get_trending_keywords(category: str = "electronics") -> list[str]:
    """Return currently trending search keywords for a product category."""
    TRENDING = {
        "electronics": ["wireless earbuds india", "65 inch tv", "gaming laptop under 80000",
                        "iphone 15 price", "smartwatch under 5000"],
        "fashion":     ["oversized t-shirt men", "linen trousers women", "white sneakers",
                        "ethnic wear kurta men", "coquette fashion"],
        "appliances":  ["air fryer india", "inverter ac 1.5 ton", "water purifier ro uv",
                        "front load washing machine", "robot vacuum India"],
        "fmcg":        ["niacinamide serum india", "vitamin c face wash",
                        "protein powder veg", "green tea brand india", "ayurvedic face cream"],
        "sports":      ["yoga mat premium", "gym gloves leather", "skipping rope speed",
                        "cricket bat players edition", "cycling helmet India"],
    }
    return TRENDING.get(category.lower(), TRENDING["electronics"])
