"""
PriceRadar — FastAPI Application Entry Point
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers.prices import router as prices_router
from routers.trends import router as trends_router
from routers.inventory import router as inventory_router

app = FastAPI(
    title="PriceRadar API",
    description="Real-Time Competitive Price Intelligence for Retailers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS (allow frontend on any origin during hackathon) ──────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from fastapi.staticfiles import StaticFiles

# ── Routes ────────────────────────────────────────────────────────
app.include_router(prices_router)
app.include_router(trends_router)
app.include_router(inventory_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "PriceRadar API"}

# ── Frontend Integration ──────────────────────────────────────────
# Serve the frontend HTML/CSS/JS directly from the FastAPI server (MUST BE LAST)
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
