"""
PriceRadar — Inventory Mock Data Engine (FMCG Focus)
Generates stock levels and 7-day demand forecasts for supermarket goods.
"""

import math
import random
from typing import List, Dict

# D-Mart style FMCG products
FMCG_SKUS = [
    # Grains
    {"id": "FMCG_001", "name": "India Gate Basmati Rice 5kg", "category": "Grains"},
    {"id": "FMCG_002", "name": "Aashirvaad Atta 10kg", "category": "Grains"},
    {"id": "FMCG_013", "name": " आशीर्वाद  Atta 5kg", "category": "Grains"},
    {"id": "FMCG_016", "name": "Toor Dal Premium 1kg", "category": "Grains"},
    
    # Vegetables
    {"id": "FMCG_017", "name": "Fresh Tomatoes 1kg", "category": "Vegetables"},
    {"id": "FMCG_018", "name": "Onions 1kg", "category": "Vegetables"},
    {"id": "FMCG_019", "name": "Potatoes 1kg", "category": "Vegetables"},
    {"id": "FMCG_020", "name": "Fresh Coriander 100g", "category": "Vegetables"},

    # Other Groceries
    {"id": "FMCG_003", "name": "Fortune Sunflower Oil 5L", "category": "Grocery"},
    {"id": "FMCG_004", "name": "Maggi 2-Minute Noodles 12-Pack", "category": "Packaged Food"},
    {"id": "FMCG_005", "name": "Surf Excel Matic Front Load 2kg", "category": "Household"},
    {"id": "FMCG_006", "name": "Colgate MaxFresh Toothpaste 150g", "category": "Personal Care"},
    {"id": "FMCG_007", "name": "Tata Salt 1kg", "category": "Grocery"},
    {"id": "FMCG_008", "name": "Parle-G Gold Biscuits 1kg", "category": "Packaged Food"},
    {"id": "FMCG_009", "name": "Dettol Liquid Handwash 200ml", "category": "Personal Care"},
    {"id": "FMCG_010", "name": "Amul Butter 500g", "category": "Dairy"},
    {"id": "FMCG_011", "name": "Lipton Green Tea 100 Bags", "category": "Beverages"},
    {"id": "FMCG_012", "name": "Vim Dishwash Gel 500ml", "category": "Household"},
    {"id": "FMCG_014", "name": "Nutella Hazelnut Spread 350g", "category": "Packaged Food"},
    {"id": "FMCG_015", "name": "Britannia Good Day 250g", "category": "Packaged Food"},
]

STORES = [
    {"id": "STR_001", "name": "Store 001 (Main Branch)"},
    {"id": "STR_002", "name": "Store 002"},
    {"id": "STR_003", "name": "Store 003"},
    {"id": "STR_004", "name": "Store 004"},
    {"id": "STR_005", "name": "Store 005"},
]

# Generate static seed data to keep demo consistent
random.seed(42)

def generate_inventory_database() -> Dict:
    db = {}
    for store in STORES:
        store_inventory = {}
        for sku in FMCG_SKUS:
            # Randomize current stock
            base_stock = random.randint(10, 800)
            
            # Categorize stock amount
            if base_stock > 300:
                stock_level = "High"
            elif base_stock >= 100:
                stock_level = "Medium"
            else:
                stock_level = "Low"

            # Generate demand forecast (7 days)
            avg_daily_demand = random.uniform(5.0, 150.0)
            
            # Ensure some low-stock items have high demand to create "High Risk" scenarios
            if stock_level == "Low" and random.random() > 0.5:
                avg_daily_demand = random.uniform(40.0, 90.0)

            forecast = []
            for day in range(7):
                # Add day-of-week seasonality (weekends higher)
                multiplier = random.uniform(0.8, 1.2)
                if day in [5, 6]:  # Weekend proxy
                    multiplier *= 1.4
                daily_val = int(avg_daily_demand * multiplier)
                forecast.append(max(0, daily_val))
            
            total_7_day_demand = sum(forecast)
            
            # Stockout Risk Logic
            if total_7_day_demand > base_stock * 1.1:
                risk = "HIGH"
            elif total_7_day_demand > base_stock * 0.7:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            stock_coverage_pct = round((base_stock / max(1, total_7_day_demand)) * 100)
            reorder_qty = max(0, int((total_7_day_demand * 1.5) - base_stock))

            store_inventory[sku["id"]] = {
                "sku_details": sku,
                "current_stock": base_stock,
                "stock_level_badge": stock_level,
                "forecast_7_day": forecast,
                "total_7_day_demand": total_7_day_demand,
                "avg_daily_demand": round(sum(forecast) / 7.0, 1),
                "risk_status": risk,
                "coverage_pct": stock_coverage_pct,
                "reorder_qty": reorder_qty
            }
        db[store["id"]] = store_inventory
    return db

# Cache database
_INVENTORY_DB = generate_inventory_database()


def get_all_stores() -> List[Dict]:
    return STORES

def get_skus_for_store(store_id: str) -> List[Dict]:
    if store_id not in _INVENTORY_DB:
        return []
    
    # Return basic info for dropdowns
    result = []
    for sku_id, data in _INVENTORY_DB[store_id].items():
        result.append(data["sku_details"])
    return result

def get_forecast_for_sku(store_id: str, sku_id: str) -> Dict:
    if store_id not in _INVENTORY_DB or sku_id not in _INVENTORY_DB[store_id]:
        return None
    
    item = _INVENTORY_DB[store_id][sku_id]
    
    # Generate daily simulated "running stock" line
    running_stock = []
    current = item["current_stock"]
    for demand in item["forecast_7_day"]:
        current = max(0, current - demand)
        running_stock.append(current)

    return {
        "store_id": store_id,
        "sku": item["sku_details"],
        "metrics": {
            "current_stock": item["current_stock"],
            "stock_level": item["stock_level_badge"],
            "total_7_day_demand": item["total_7_day_demand"],
            "avg_daily_demand": item["avg_daily_demand"],
            "coverage_pct": item["coverage_pct"],
            "reorder_qty": item["reorder_qty"],
            "risk_status": item["risk_status"]
        },
        "charts": {
            "forecast_demand": item["forecast_7_day"],
            "running_stock": running_stock
        }
    }

def get_risk_summary(store_id: str = None) -> List[Dict]:
    """Returns flat list for the risk summary table."""
    summary = []
    
    stores_to_process = [store_id] if store_id else [s["id"] for s in STORES]
    
    for sid in stores_to_process:
        if sid not in _INVENTORY_DB:
            continue
            
        store_name = next(s["name"] for s in STORES if s["id"] == sid)
        
        for sku_id, data in _INVENTORY_DB[sid].items():
            summary.append({
                "store_name": store_name,
                "sku_id": data["sku_details"]["id"],
                "sku_name": data["sku_details"]["name"],
                "category": data["sku_details"]["category"],
                "current_stock": data["current_stock"],
                "stock_level": data["stock_level_badge"],
                "total_demand": data["total_7_day_demand"],
                "avg_daily": data["avg_daily_demand"],
                "risk": data["risk_status"]
            })
            
    # Sort by risk (HIGH first, then LOW stock)
    def risk_score(item):
        r_map = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        return (r_map[item["risk"]], item["stock_level"] != "Low", item["current_stock"])
        
    summary.sort(key=risk_score)
    return summary
