"""
PriceRadar — Social Media Signal Engine
Simulates TikTok viral products, Instagram trending hashtags,
Pinterest trends, and combined social buzz scores.
In production: integrate TikTok Creative Center API, Meta Ad Library, 
Pinterest Trends API.
"""

import random
from datetime import datetime, timezone

# ── TikTok Viral Products ────────────────────────────────────────
TIKTOK_VIRAL = [
    {
        "title": "Stanley Quencher Tumbler 40oz",
        "hashtag": "#stanleycup",
        "views_m":  842.5,
        "like_rate": 9.2,
        "category": "Drinkware",
        "trend_velocity": "🚀 Exploding",
        "buying_intent": "Very High",
        "mention_24h": 84200,
    },
    {
        "title": "Viral Blush & Filter Combo Set",
        "hashtag": "#blushtrend",
        "views_m":  612.0,
        "like_rate": 8.8,
        "category": "Beauty",
        "trend_velocity": "🔥 Surging",
        "buying_intent": "Very High",
        "mention_24h": 52100,
    },
    {
        "title": "LED Sunset Projector Lamp",
        "hashtag": "#sunsetlamp",
        "views_m":  490.3,
        "like_rate": 8.1,
        "category": "Home Decor",
        "trend_velocity": "📈 Rising",
        "buying_intent": "High",
        "mention_24h": 31800,
    },
    {
        "title": "Skincare Gua Sha Facial Tool",
        "hashtag": "#guasha",
        "views_m":  380.9,
        "like_rate": 7.9,
        "category": "Skincare",
        "trend_velocity": "📈 Rising",
        "buying_intent": "High",
        "mention_24h": 28400,
    },
    {
        "title": "Mini Hair Straightener Brush",
        "hashtag": "#hairbrush",
        "views_m":  290.1,
        "like_rate": 7.6,
        "category": "Hair Care",
        "trend_velocity": "➡ Steady",
        "buying_intent": "Medium",
        "mention_24h": 19200,
    },
    {
        "title": "Portable Pocket Espresso Maker",
        "hashtag": "#pocketespresso",
        "views_m":  210.4,
        "like_rate": 7.4,
        "category": "Kitchen",
        "trend_velocity": "🔥 Surging",
        "buying_intent": "High",
        "mention_24h": 14600,
    },
    {
        "title": "Bubble Wrap Fidget Phone Case",
        "hashtag": "#bubblecase",
        "views_m":  185.0,
        "like_rate": 7.1,
        "category": "Phone Accessories",
        "trend_velocity": "➡ Steady",
        "buying_intent": "Medium",
        "mention_24h": 11200,
    },
    {
        "title": "Aesthetic Planner & Journal Set",
        "hashtag": "#journaling",
        "views_m":  143.2,
        "like_rate": 8.5,
        "category": "Stationery",
        "trend_velocity": "📈 Rising",
        "buying_intent": "High",
        "mention_24h": 9800,
    },
]

# ── Instagram Trending Hashtags ───────────────────────────────────
INSTAGRAM_TRENDING = [
    {"hashtag": "#tiktokmademebuyit",   "posts_m": 8.2,  "engagement": "Very High", "category": "General",    "sentiment": "Positive"},
    {"hashtag": "#unboxing",            "posts_m": 4.1,  "engagement": "High",      "category": "General",    "sentiment": "Positive"},
    {"hashtag": "#aestheticroom",       "posts_m": 3.8,  "engagement": "High",      "category": "Home Decor", "sentiment": "Positive"},
    {"hashtag": "#skincareroutine",     "posts_m": 6.2,  "engagement": "Very High", "category": "Beauty",     "sentiment": "Positive"},
    {"hashtag": "#fitcheck",            "posts_m": 5.1,  "engagement": "Very High", "category": "Fashion",    "sentiment": "Positive"},
    {"hashtag": "#techreview",          "posts_m": 2.9,  "engagement": "Medium",    "category": "Electronics","sentiment": "Mixed"},
    {"hashtag": "#gymlife",             "posts_m": 7.4,  "engagement": "Very High", "category": "Fitness",    "sentiment": "Positive"},
    {"hashtag": "#homeorganization",    "posts_m": 3.2,  "engagement": "High",      "category": "Home",       "sentiment": "Positive"},
]

# ── Pinterest Trends ──────────────────────────────────────────────
PINTEREST_TRENDS = [
    {"keyword": "Cottagecore Bedroom Decor",   "monthly_searches_k": 891, "yoy_growth": "+128%", "category": "Home Decor", "season": "All Year"},
    {"keyword": "Quiet Luxury Aesthetic",       "monthly_searches_k": 720, "yoy_growth": "+214%", "category": "Fashion",   "season": "Current"},
    {"keyword": "Boho Wedding Inspiration",     "monthly_searches_k": 640, "yoy_growth": "+89%",  "category": "Events",    "season": "Mar–Jun"},
    {"keyword": "Minimalist Kitchen Shelving",  "monthly_searches_k": 520, "yoy_growth": "+76%",  "category": "Home",      "season": "All Year"},
    {"keyword": "Coquette Fashion Summer",      "monthly_searches_k": 480, "yoy_growth": "+310%", "category": "Fashion",   "season": "Current"},
    {"keyword": "Terracotta Home Accessories",  "monthly_searches_k": 390, "yoy_growth": "+58%",  "category": "Home Decor","season": "All Year"},
    {"keyword": "Dark Academia Outfits",        "monthly_searches_k": 340, "yoy_growth": "+92%",  "category": "Fashion",   "season": "Sep–Feb"},
    {"keyword": "Eco-Friendly Gift Ideas",      "monthly_searches_k": 290, "yoy_growth": "+45%",  "category": "Gifts",     "season": "Nov–Jan"},
]


def get_tiktok_viral() -> list:
    return TIKTOK_VIRAL


def get_instagram_trending() -> list:
    return INSTAGRAM_TRENDING


def get_pinterest_trends() -> list:
    return PINTEREST_TRENDS


def get_social_buzz(product_name: str, category: str = "") -> dict:
    """
    Return a social buzz profile for a given product name.
    Combines TikTok mentions, Instagram engagement, and Pinterest search volume.
    """
    rng = random.Random(hash(f"{product_name}-{category}") & 0xFFFF)

    tiktok_views_m   = round(rng.uniform(5, 220), 1)
    ig_posts_k       = round(rng.uniform(10, 800), 0)
    pinterest_saves_k = round(rng.uniform(5, 300), 0)

    # Weighted buzz score
    buzz = min(100, int(
        (tiktok_views_m / 220) * 40
        + (ig_posts_k / 800) * 35
        + (pinterest_saves_k / 300) * 25
    ))

    hashtags = [
        f"#{product_name.lower().replace(' ', '')}",
        "#unboxing",
        "#productreview" if "electronics" in category.lower() else "#trending",
    ]

    return {
        "buzz_score":       buzz,
        "tiktok_views_m":   tiktok_views_m,
        "ig_posts_k":       ig_posts_k,
        "pinterest_saves_k": pinterest_saves_k,
        "trending_hashtags": hashtags,
        "virality": "🚀 Viral" if buzz >= 70 else "🔥 Buzzing" if buzz >= 50 else "📢 Mentioned",
    }
