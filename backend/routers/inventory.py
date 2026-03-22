"""
PriceRadar — Inventory API Router
Endpoints for fetching FMCG inventory forecasts and stockout risk summaries.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from data.inventory import (
    get_all_stores,
    get_skus_for_store,
    get_forecast_for_sku,
    get_risk_summary
)

router = APIRouter(prefix="/api/inventory", tags=["inventory"])

@router.get("/stores")
async def fetch_stores():
    """Get list of all D-Mart style store locations."""
    return {"stores": get_all_stores()}

@router.get("/skus")
async def fetch_skus(store_id: str):
    """Get list of all FMCG SKUs tracked in a specific store."""
    skus = get_skus_for_store(store_id)
    if not skus:
        raise HTTPException(status_code=404, detail="Store not found or empty.")
    return {"skus": skus}

@router.get("/forecast")
async def fetch_forecast(store_id: str, sku_id: str):
    """Get the 7-day demand forecast vs stock trajectory + KPIs."""
    data = get_forecast_for_sku(store_id, sku_id)
    if not data:
        raise HTTPException(status_code=404, detail="Store or SKU not found.")
    return data

@router.get("/summary")
async def fetch_summary(store_id: Optional[str] = None):
    """
    Get the top stockout risks across all SKUs, 
    optionally filtered by a single store.
    """
    summary = get_risk_summary(store_id)
    return {"items": summary}
