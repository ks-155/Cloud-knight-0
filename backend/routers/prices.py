"""
PriceRadar — API Routes
Endpoints for product search, competitor prices, history, and
ML-powered price recommendations.
"""

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone

from data.products import search_products, get_product, CATEGORY_ELASTICITY
from data.market import get_competitor_prices, get_price_history, get_demand_signals
from ml.model import recommend_price

router = APIRouter(prefix="/api", tags=["prices"])


# ── Request / Response Models ─────────────────────────────────────
class RecommendRequest(BaseModel):
    product_id: str
    your_price: float
    cost_price: float


# ── Endpoints ────────────────────────────────────────────────────
@router.get("/products/search")
async def search(q: str = Query(default="", description="Product search query")):
    """Search for products by name, brand, or category."""
    results = search_products(q)
    return {
        "query": q,
        "count": len(results),
        "products": results,
    }


@router.get("/products/{product_id}")
async def get_product_detail(product_id: str):
    """Get full details of a single product."""
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/prices/{product_id}")
async def get_prices(
    product_id: str,
    your_price: float = Query(default=None, description="Your current price for comparison"),
):
    """
    Get current competitor prices for a product, plus market stats
    and demand signals. Optionally compare against your price.
    """
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    data = get_competitor_prices(product, your_price=your_price)
    return data


@router.get("/history/{product_id}")
async def get_history(
    product_id: str,
    days: int = Query(default=7, ge=3, le=30, description="Number of days of history"),
):
    """Get price history over the last N days for all competitors."""
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    history = get_price_history(product, days=days)
    return {
        "product_id": product_id,
        "days": days,
        "history": history,
    }


@router.post("/recommend")
async def get_recommendation(body: RecommendRequest):
    """
    POST { product_id, your_price }
    Returns AI-powered optimal price recommendation.
    """
    product = get_product(body.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if body.your_price <= 0 or body.cost_price <= 0:
        raise HTTPException(status_code=400, detail="prices must be positive")

    # Get market data
    market = get_competitor_prices(product, your_price=body.your_price)
    stats = market["market_stats"]
    signals = market["demand_signals"]
    dt = datetime.now(timezone.utc)

    # Count competitors cheaper than you
    comp_below = sum(
        1 for c in market["competitors"] if c["price"] < body.your_price
    )

    # Days until next festival (simplified)
    days_festival = 30
    for month, day, *_ in [
        (10, 20), (1, 1), (12, 25), (8, 15), (1, 26), (6, 21)
    ]:
        try:
            fest_dt = dt.replace(month=month, day=day)
            diff = (fest_dt - dt).days
            if 0 <= diff < days_festival:
                days_festival = diff
        except ValueError:
            pass

    recommendation = recommend_price(
        your_price=body.your_price,
        cost_price=body.cost_price,
        competitor_avg=stats["average"],
        spread_pct=stats["spread_pct"],
        demand_signal=signals["overall_demand"],
        day_of_week=dt.weekday(),
        days_until_festival=days_festival,
        category_elasticity=CATEGORY_ELASTICITY.get(product["category"], 0.5),
        competitors_below_you=comp_below,
    )

    return {
        "product_id": body.product_id,
        "product_name": product["name"],
        "your_price": body.your_price,
        "market_avg": stats["average"],
        "market_lowest": stats["lowest"],
        "recommendation": recommendation,
        "demand_signals": signals,
    }


@router.get("/signals")
async def market_signals():
    """Get current market demand signals (festival, day-of-week, etc.)"""
    return get_demand_signals()


@router.get("/demo")
async def demo_products():
    """Returns 5 hand-picked demo products for the 'Try Demo' button."""
    demo_ids = ["ELEC001", "ELEC003", "APPL002", "FASH001", "FMCG001"]
    products = [get_product(pid) for pid in demo_ids]
    return {"products": [p for p in products if p]}
