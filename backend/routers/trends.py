"""
PriceRadar — Trends API Router
Endpoints for Google Trends, bestseller lists, and social signals.
"""

from fastapi import APIRouter, Query
from data.trends import get_amazon_movers, get_etsy_trending, get_ebay_watched, get_platform_trend_score
from data.social import get_tiktok_viral, get_instagram_trending, get_pinterest_trends, get_social_buzz
from ml.google_trends import get_google_trends, get_trending_keywords

router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.get("/google")
async def google_trends(
    keyword: str = Query(..., description="Search keyword, e.g. 'Samsung TV'"),
    timeframe: str = Query(default="today 7-d", description="pytrends timeframe string"),
):
    """
    Fetch Google Trends interest over time for a keyword (India locale).
    Uses pytrends with synthetic fallback if rate-limited.
    """
    data = get_google_trends(keyword, timeframe)
    return data


@router.get("/keywords")
async def trending_keywords(
    category: str = Query(default="electronics", description="Product category"),
):
    """Return trending search keywords for a product category."""
    keywords = get_trending_keywords(category)
    return {"category": category, "keywords": keywords}


@router.get("/bestsellers")
async def bestsellers(
    platform: str = Query(default="amazon", description="Platform: amazon | etsy | ebay"),
    category: str = Query(default="Electronics", description="Product category (Amazon only)"),
):
    """
    Fetch bestseller / most-watched lists from Amazon, Etsy, or eBay.
    """
    platform = platform.lower()
    if platform == "amazon":
        items = get_amazon_movers(category)
        return {"platform": "Amazon India",  "list_type": "Movers & Shakers", "category": category, "items": items}
    elif platform == "etsy":
        items = get_etsy_trending()
        return {"platform": "Etsy",          "list_type": "Trending Now",     "category": "All",     "items": items}
    elif platform == "ebay":
        items = get_ebay_watched()
        return {"platform": "eBay",          "list_type": "Most Watched",     "category": "All",     "items": items}
    else:
        return {"error": "Unknown platform. Use: amazon | etsy | ebay"}


@router.get("/social")
async def social_signals(
    product_name: str = Query(..., description="Product name to look up"),
    category: str = Query(default="", description="Optional product category"),
):
    """Get social media buzz analysis for a given product."""
    buzz   = get_social_buzz(product_name, category)
    tiktok = get_tiktok_viral()[:3]   # Top 3 most comparable viral items
    return {
        "product": product_name,
        "buzz":    buzz,
        "tiktok_top_trends": tiktok,
    }


@router.get("/tiktok")
async def tiktok_viral():
    """Full TikTok viral product list."""
    return {"items": get_tiktok_viral()}


@router.get("/instagram")
async def instagram_trending():
    """Instagram trending hashtags."""
    return {"hashtags": get_instagram_trending()}


@router.get("/pinterest")
async def pinterest_trends():
    """Pinterest trending search keywords."""
    return {"trends": get_pinterest_trends()}


@router.get("/score/{product_id}")
async def trend_score(product_id: str):
    """
    Get a cross-platform trend score for a specific product by ID.
    Used to display trend badges on the competitor price table.
    """
    from data.products import get_product
    product = get_product(product_id)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    score = get_platform_trend_score(product["name"])
    buzz  = get_social_buzz(product["name"], product["category"])
    return {
        "product_id":   product_id,
        "product_name": product["name"],
        "trend_score":  score,
        "social_buzz":  buzz,
    }


@router.get("/overview")
async def trends_overview():
    """
    Full trend intelligence overview — top picks from each source.
    Used to populate the Trends dashboard tab on first load.
    """
    return {
        "tiktok_viral":       get_tiktok_viral()[:5],
        "instagram_trending": get_instagram_trending()[:5],
        "pinterest_trends":   get_pinterest_trends()[:5],
        "amazon_movers":      get_amazon_movers("Electronics")[:5],
        "etsy_trending":      get_etsy_trending()[:4],
        "ebay_watched":       get_ebay_watched()[:4],
    }
