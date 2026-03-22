"""
PriceRadar — Product Catalog
20+ realistic Indian retail products across 5 categories.
"""

PRODUCTS = [
    # ── Electronics ──────────────────────────────────────────────
    {
        "id": "ELEC001",
        "name": "Samsung 65-inch 4K QLED Smart TV",
        "brand": "Samsung",
        "category": "Electronics",
        "base_price": 72000,
        "unit": "piece",
        "keywords": ["samsung", "tv", "television", "65 inch", "qled", "4k", "smart tv"],
    },
    {
        "id": "ELEC002",
        "name": "Sony 55-inch OLED Android TV",
        "brand": "Sony",
        "category": "Electronics",
        "base_price": 89000,
        "unit": "piece",
        "keywords": ["sony", "tv", "oled", "55 inch", "android tv"],
    },
    {
        "id": "ELEC003",
        "name": "Apple iPhone 15 Pro 256GB",
        "brand": "Apple",
        "category": "Electronics",
        "base_price": 134900,
        "unit": "piece",
        "keywords": ["iphone", "apple", "15 pro", "smartphone", "mobile"],
    },
    {
        "id": "ELEC004",
        "name": "Samsung Galaxy S24 Ultra 512GB",
        "brand": "Samsung",
        "category": "Electronics",
        "base_price": 109999,
        "unit": "piece",
        "keywords": ["samsung", "galaxy", "s24", "android", "smartphone", "mobile"],
    },
    {
        "id": "ELEC005",
        "name": "OnePlus 12 5G 256GB",
        "brand": "OnePlus",
        "category": "Electronics",
        "base_price": 64999,
        "unit": "piece",
        "keywords": ["oneplus", "12", "5g", "smartphone", "mobile", "android"],
    },
    {
        "id": "ELEC006",
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "brand": "Sony",
        "category": "Electronics",
        "base_price": 26990,
        "unit": "piece",
        "keywords": ["sony", "headphones", "wh1000xm5", "noise cancelling", "wireless"],
    },
    {
        "id": "ELEC007",
        "name": "Apple MacBook Air M3 8GB 256GB",
        "brand": "Apple",
        "category": "Electronics",
        "base_price": 114900,
        "unit": "piece",
        "keywords": ["macbook", "apple", "laptop", "m3", "air"],
    },
    {
        "id": "ELEC008",
        "name": "Dell XPS 15 Intel i7 16GB 512GB",
        "brand": "Dell",
        "category": "Electronics",
        "base_price": 139990,
        "unit": "piece",
        "keywords": ["dell", "xps", "laptop", "i7", "windows"],
    },
    # ── Home Appliances ──────────────────────────────────────────
    {
        "id": "APPL001",
        "name": "LG 260L Double Door Frost-Free Refrigerator",
        "brand": "LG",
        "category": "Appliances",
        "base_price": 28990,
        "unit": "piece",
        "keywords": ["lg", "refrigerator", "fridge", "double door", "260l"],
    },
    {
        "id": "APPL002",
        "name": "Samsung 8kg Front Load Washing Machine",
        "brand": "Samsung",
        "category": "Appliances",
        "base_price": 34990,
        "unit": "piece",
        "keywords": ["samsung", "washing machine", "front load", "8kg"],
    },
    {
        "id": "APPL003",
        "name": "Dyson V15 Detect Cordless Vacuum Cleaner",
        "brand": "Dyson",
        "category": "Appliances",
        "base_price": 52900,
        "unit": "piece",
        "keywords": ["dyson", "vacuum", "v15", "cordless", "cleaner"],
    },
    {
        "id": "APPL004",
        "name": "Voltas 1.5 Ton 5 Star Inverter Split AC",
        "brand": "Voltas",
        "category": "Appliances",
        "base_price": 38990,
        "unit": "piece",
        "keywords": ["voltas", "ac", "air conditioner", "1.5 ton", "inverter", "split"],
    },
    {
        "id": "APPL005",
        "name": "Instant Pot Duo 7-in-1 Electric Pressure Cooker",
        "brand": "Instant Pot",
        "category": "Appliances",
        "base_price": 7990,
        "unit": "piece",
        "keywords": ["instant pot", "pressure cooker", "electric", "cooker"],
    },
    # ── Fashion ──────────────────────────────────────────────────
    {
        "id": "FASH001",
        "name": "Nike Air Max 270 Running Shoes",
        "brand": "Nike",
        "category": "Fashion",
        "base_price": 9995,
        "unit": "pair",
        "keywords": ["nike", "air max", "shoes", "running", "sneakers"],
    },
    {
        "id": "FASH002",
        "name": "Levi's 501 Original Fit Jeans",
        "brand": "Levi's",
        "category": "Fashion",
        "base_price": 3499,
        "unit": "pair",
        "keywords": ["levis", "levi's", "jeans", "501", "denim"],
    },
    {
        "id": "FASH003",
        "name": "Ray-Ban Aviator Classic Sunglasses",
        "brand": "Ray-Ban",
        "category": "Fashion",
        "base_price": 7490,
        "unit": "piece",
        "keywords": ["rayban", "ray-ban", "sunglasses", "aviator", "classic"],
    },
    # ── Groceries (Grains, Vegetables, FMCG) ─────────────────────
    {
        "id": "GRN001",
        "name": "India Gate Basmati Rice 5kg",
        "brand": "India Gate",
        "category": "Grains",
        "base_price": 550,
        "unit": "pack",
        "keywords": ["rice", "basmati", "india gate", "grains", "food"],
    },
    {
        "id": "GRN002",
        "name": "Aashirvaad Atta 10kg",
        "brand": "Aashirvaad",
        "category": "Grains",
        "base_price": 425,
        "unit": "pack",
        "keywords": ["atta", "flour", "wheat", "aashirvaad", "grains"],
    },
    {
        "id": "VEG001",
        "name": "Fresh Tomatoes 1kg",
        "brand": "Local Farms",
        "category": "Vegetables",
        "base_price": 60,
        "unit": "kg",
        "keywords": ["tomato", "tomatoes", "veg", "vegetables", "fresh"],
    },
    {
        "id": "VEG002",
        "name": "Fresh Onions 1kg",
        "brand": "Local Farms",
        "category": "Vegetables",
        "base_price": 40,
        "unit": "kg",
        "keywords": ["onion", "onions", "veg", "vegetables", "fresh"],
    },
    {
        "id": "FMCG001",
        "name": "Nescafe Gold Premium Instant Coffee 200g",
        "brand": "Nescafe",
        "category": "Household",
        "base_price": 599,
        "unit": "pack",
        "keywords": ["nescafe", "coffee", "instant", "gold", "nestle"],
    },
    {
        "id": "FMCG002",
        "name": "Himalaya Face Wash Neem Purifying 150ml",
        "brand": "Himalaya",
        "category": "FMCG",
        "base_price": 175,
        "unit": "bottle",
        "keywords": ["himalaya", "face wash", "neem", "purifying"],
    },
    {
        "id": "FMCG003",
        "name": "Dove Moisturizing Body Lotion 400ml",
        "brand": "Dove",
        "category": "FMCG",
        "base_price": 299,
        "unit": "bottle",
        "keywords": ["dove", "lotion", "body lotion", "moisturizing"],
    },
    # ── Sports & Fitness ─────────────────────────────────────────
    {
        "id": "SPRT001",
        "name": "Decathlon Domyos Weight Training Dumbbell Set 20kg",
        "brand": "Decathlon",
        "category": "Sports",
        "base_price": 2499,
        "unit": "set",
        "keywords": ["decathlon", "dumbbell", "weights", "gym", "fitness", "training"],
    },
    {
        "id": "SPRT002",
        "name": "Fitbit Charge 6 Advanced Fitness Tracker",
        "brand": "Fitbit",
        "category": "Sports",
        "base_price": 14999,
        "unit": "piece",
        "keywords": ["fitbit", "fitness tracker", "smartband", "health", "charge 6"],
    },
]


def search_products(query: str) -> list:
    """Return products matching the query string (fuzzy keyword match)."""
    q = query.lower().strip()
    if not q:
        return PRODUCTS

    results = []
    for p in PRODUCTS:
        # Check name, brand, category, keywords
        if (
            q in p["name"].lower()
            or q in p["brand"].lower()
            or q in p["category"].lower()
            or any(q in kw for kw in p["keywords"])
        ):
            results.append(p)

    return results[:10]


def get_product(product_id: str) -> dict | None:
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


CATEGORY_ELASTICITY = {
    "Electronics": 0.65,   # High elasticity — buyers compare a lot
    "Appliances":  0.55,
    "Fashion":     0.45,
    "FMCG":        0.25,   # Low elasticity — brand loyalty
    "Sports":      0.50,
}
