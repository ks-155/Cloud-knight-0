"""
PriceRadar — Bestseller & Trending Products Data Engine
Realistic mock data for Amazon, Etsy, and eBay trending lists.
In production: replace with Jungle Scout API / Etsy API / eBay Finding API.
"""

import random
from datetime import datetime, timezone

# ── Amazon Movers & Shakers ───────────────────────────────────────
AMAZON_MOVERS = {
    "Electronics": [
        {"rank": 1,  "rank_change": "+842%", "asin": "B0CX44DFCC", "title": "boAt Airdopes Alpha Wireless Earbuds", "brand": "boAt", "price": 1299,  "rating": 4.2, "reviews": 12480, "badge": "🔥 Bestseller"},
        {"rank": 2,  "rank_change": "+612%", "asin": "B0CX59HKL9", "title": "OnePlus Nord Buds 3 Pro", "brand": "OnePlus", "price": 2999, "rating": 4.4, "reviews": 8921,  "badge": "🚀 Mover"},
        {"rank": 3,  "rank_change": "+490%", "asin": "B0CXR3JKPD", "title": "Redmi Buds 5 Pro ANC", "brand": "Redmi",  "price": 1699, "rating": 4.1, "reviews": 5632,  "badge": "📈 Rising"},
        {"rank": 4,  "rank_change": "+380%", "asin": "B0D1JK8XLM", "title": "Fire-Boltt Phoenix Ultra Smartwatch", "brand": "Fire-Boltt", "price": 1799, "rating": 3.9, "reviews": 22100, "badge": "🔥 Bestseller"},
        {"rank": 5,  "rank_change": "+310%", "asin": "B0CRV9NMKP", "title": "realme TechLife Watch S100", "brand": "realme", "price": 2199, "rating": 4.0, "reviews": 7834,  "badge": "📈 Rising"},
        {"rank": 6,  "rank_change": "+270%", "asin": "B0D2LK7PQR", "title": "Philips HF3505 Wake-Up Light Alarm", "brand": "Philips", "price": 4299, "rating": 4.5, "reviews": 3210,  "badge": "✨ New"},
        {"rank": 7,  "rank_change": "+195%", "asin": "B0CRTVZMNP", "title": "TP-Link Tapo C210 Pan-Tilt Home Camera", "brand": "TP-Link", "price": 1799, "rating": 4.3, "reviews": 18400, "badge": "🔥 Bestseller"},
        {"rank": 8,  "rank_change": "+160%", "asin": "B0D5XK9JQZ", "title": "Anker 65W GaN USB-C Charger", "brand": "Anker",  "price": 1299, "rating": 4.6, "reviews": 9200,  "badge": "🚀 Mover"},
    ],
    "Appliances": [
        {"rank": 1,  "rank_change": "+720%", "asin": "B0CX7RDMNK", "title": "Pigeon by Stovekraft Smart Air Fryer 4.2L", "brand": "Pigeon", "price": 2499, "rating": 4.1, "reviews": 31200, "badge": "🔥 Bestseller"},
        {"rank": 2,  "rank_change": "+540%", "asin": "B0D3NKL6PQ", "title": "Butterfly Smart 1.8L Electric Kettle", "brand": "Butterfly", "price": 699,  "rating": 4.3, "reviews": 14500, "badge": "🚀 Mover"},
        {"rank": 3,  "rank_change": "+390%", "asin": "B0CRVMKZPQ", "title": "Havells Fresco 1200W Mixer Grinder", "brand": "Havells", "price": 3299, "rating": 4.4, "reviews": 8900, "badge": "📈 Rising"},
        {"rank": 4,  "rank_change": "+290%", "asin": "B0D1LPKMNR", "title": "Crompton Energion HS 1200mm Ceiling Fan", "brand": "Crompton", "price": 3599, "rating": 4.2, "reviews": 5600, "badge": "✨ New"},
        {"rank": 5,  "rank_change": "+210%", "asin": "B0CRX4NKQL", "title": "Eureka Forbes Aquaguard Sure RO+UV Purifier", "brand": "Eureka Forbes", "price": 8999, "rating": 4.0, "reviews": 12300, "badge": "🔥 Bestseller"},
    ],
    "Fashion": [
        {"rank": 1,  "rank_change": "+980%", "asin": "B0CX8PLMNQ", "title": "WROGN Regular Fit Casual Oversized Shirt", "brand": "WROGN", "price": 699,  "rating": 3.8, "reviews": 42100, "badge": "🔥 Bestseller"},
        {"rank": 2,  "rank_change": "+670%", "asin": "B0D3QKJMPR", "title": "Campus Macho Running Shoe Men", "brand": "Campus", "price": 1099, "rating": 4.0, "reviews": 28700, "badge": "🚀 Mover"},
        {"rank": 3,  "rank_change": "+420%", "asin": "B0CRWNLKPQ", "title": "Roadster Men's Slim Fit Jeans", "brand": "Roadster", "price": 899,  "rating": 3.9, "reviews": 19800, "badge": "📈 Rising"},
        {"rank": 4,  "rank_change": "+310%", "asin": "B0D1MPKQRL", "title": "ONLY Women's Maxi Floral Dress", "brand": "ONLY", "price": 1299, "rating": 4.1, "reviews": 8900, "badge": "✨ New"},
    ],
    "FMCG": [
        {"rank": 1,  "rank_change": "+560%", "asin": "B0CX9QLMPR", "title": "Tata Consumer Soulfull Millet Muesli 400g", "brand": "Tata", "price": 199, "rating": 4.4, "reviews": 18200, "badge": "🔥 Bestseller"},
        {"rank": 2,  "rank_change": "+430%", "asin": "B0D4RKJNQP", "title": "Mamaearth Vitamin C Face Serum 30ml", "brand": "Mamaearth", "price": 349, "rating": 4.2, "reviews": 52100, "badge": "🚀 Mover"},
        {"rank": 3,  "rank_change": "+320%", "asin": "B0CRX6NKPL", "title": "Plum 10% Niacinamide Face Serum 30ml", "brand": "Plum", "price": 399, "rating": 4.3, "reviews": 31400, "badge": "📈 Rising"},
    ],
    "Sports": [
        {"rank": 1,  "rank_change": "+710%", "asin": "B0CXA7LMNQ", "title": "Cosco Dare Basketball Size 7", "brand": "Cosco", "price": 699,  "rating": 4.1, "reviews": 9800, "badge": "🔥 Bestseller"},
        {"rank": 2,  "rank_change": "+490%", "asin": "B0D3SKJNPR", "title": "Boldfit Gym Gloves Full Finger", "brand": "Boldfit", "price": 299,  "rating": 4.0, "reviews": 22400, "badge": "🚀 Mover"},
        {"rank": 3,  "rank_change": "+360%", "asin": "B0CRXANKLP", "title": "Strauss Yoga Mat 6mm Anti-Slip", "brand": "Strauss", "price": 499,  "rating": 4.2, "reviews": 41200, "badge": "📈 Rising"},
    ],
}

# ── Etsy Trending (Niche / Handmade) ─────────────────────────────
ETSY_TRENDING = [
    {"title": "Personalized Sterling Silver Name Necklace", "category": "Jewellery", "price_usd": 24.99, "sales": 8420, "trending_score": 98, "tag": "🌟 Most Wished"},
    {"title": "Aesthetic Mushroom Tote Canvas Bag", "category": "Bags", "price_usd": 18.50, "sales": 6210, "trending_score": 95, "tag": "🔥 Top Pick"},
    {"title": "Cottagecore Pressed Flower Bookmark Set", "category": "Stationery", "price_usd": 8.99, "sales": 12800, "trending_score": 94, "tag": "🔥 Top Pick"},
    {"title": "Custom Pet Portrait Watercolor Print", "category": "Art Prints", "price_usd": 34.00, "sales": 5600, "trending_score": 91, "tag": "📈 Rising"},
    {"title": "Vintage-Style Tarot Card Set 78-Card Deck", "category": "Games", "price_usd": 22.00, "sales": 9100, "trending_score": 89, "tag": "📈 Rising"},
    {"title": "Hand-Poured Soy Wax Crystal Candle", "category": "Home Decor", "price_usd": 16.99, "sales": 7340, "trending_score": 87, "tag": "🌟 Most Wished"},
    {"title": "Macramé Wall Hanging Boho Decor", "category": "Home Decor", "price_usd": 29.00, "sales": 4200, "trending_score": 85, "tag": "📈 Rising"},
    {"title": "Personalized Leather Passport Holder", "category": "Travel", "price_usd": 19.99, "sales": 11200, "trending_score": 83, "tag": "🔥 Top Pick"},
]

# ── eBay Most Watched ─────────────────────────────────────────────
EBAY_MOST_WATCHED = [
    {"title": "Apple iPhone 14 128GB Unlocked — Open Box", "category": "Electronics", "watch_count": 4821, "bids": 28, "price": 42000, "price_trend": "+3.2%", "condition": "Open Box"},
    {"title": "PS5 Console Disc Edition — Bundle", "category": "Gaming", "watch_count": 3920, "bids": 14, "price": 52000, "price_trend": "-1.8%", "condition": "New"},
    {"title": "Vintage Rolex Submariner 1960s — Parts", "category": "Watches", "watch_count": 3210, "bids": 9,  "price": 180000, "price_trend": "+12.4%", "condition": "For Parts"},
    {"title": "Nike Air Jordan 1 Retro High OG Size 10", "category": "Sneakers", "watch_count": 2890, "bids": 19, "price": 14500, "price_trend": "+6.1%", "condition": "New w/o Box"},
    {"title": "GoPro Hero 12 Black Action Camera", "category": "Cameras", "watch_count": 2540, "bids": 11, "price": 31000, "price_trend": "-2.1%", "condition": "New"},
    {"title": "Rare 1990s Levi's 501 — Vintage Distressed", "category": "Fashion", "watch_count": 2180, "bids": 24, "price": 4200,  "price_trend": "+9.8%", "condition": "Used"},
    {"title": "Antique Brass Telescope — Maritime 1920s", "category": "Collectibles", "watch_count": 1960, "bids": 7,  "price": 8900,  "price_trend": "+22.0%", "condition": "Used"},
    {"title": "Dyson V11 Cordless Vacuum — Refurb", "category": "Appliances", "watch_count": 1740, "bids": 6,  "price": 22000, "price_trend": "-4.5%", "condition": "Refurbished"},
]


def get_amazon_movers(category: str = "Electronics") -> list:
    cat = category.title()
    return AMAZON_MOVERS.get(cat, AMAZON_MOVERS["Electronics"])


def get_etsy_trending() -> list:
    return ETSY_TRENDING


def get_ebay_watched() -> list:
    return EBAY_MOST_WATCHED


def get_platform_trend_score(product_name: str) -> dict:
    """
    Return a synthesized 'Trend Score' (0–100) for a given product,
    simulating cross-platform trending signals.
    """
    rng = random.Random(hash(product_name.lower()) & 0xFFFFFF)
    base   = rng.randint(45, 85)
    amazon = min(100, base + rng.randint(-10, 20))
    etsy   = min(100, base + rng.randint(-15, 15))
    ebay   = min(100, base + rng.randint(-12, 18))
    overall = round((amazon + etsy + ebay) / 3)
    direction = "rising" if rng.random() > 0.35 else "stable"
    return {
        "overall_score": overall,
        "direction":     direction,
        "amazon_score":  amazon,
        "etsy_score":    etsy,
        "ebay_score":    ebay,
        "label": "🔥 Hot" if overall >= 75 else "📈 Rising" if overall >= 60 else "➡ Steady",
    }
