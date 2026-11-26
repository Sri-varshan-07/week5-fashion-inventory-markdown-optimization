"""
Production REST API for Fashion Prescriptive Inventory & Markdown Optimization.
Built with FastAPI for real-time merchandising decision support.
"""

import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd

from src.data_loader import load_catalog_metadata
from src.inventory_engine import FashionInventoryOptimizer
from src.markdown_engine import DynamicMarkdownEngine

app = FastAPI(
    title="Fashion Trend & Inventory Decision Support API",
    description="Prescriptive Analytics, Newsvendor Optimization, and Dynamic Markdown Scheduling for Apparel Merchandising.",
    version="1.0.0",
)

# Initialize engines
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
catalog_df = load_catalog_metadata(base_path=BASE_DIR)
inventory_optimizer = FashionInventoryOptimizer(catalog_df)
markdown_engine = DynamicMarkdownEngine(catalog_df)


# --- Request & Response Schemas ---

class InventoryRequest(BaseModel):
    category: str = Field(..., example="Oversized Blazers")
    predicted_mean_index: float = Field(..., ge=0.0, example=55.5)
    lower_80_index: float = Field(..., ge=0.0, example=49.9)
    upper_80_index: float = Field(..., ge=0.0, example=57.5)
    scale_factor: float = Field(default=100.0, example=100.0)


class InventoryResponse(BaseModel):
    category: str
    sku: str
    retail_price: float
    unit_cost: float
    critical_fractile: float
    expected_demand_units: int
    optimal_order_quantity_Q: int
    pre_commitment_overseas_60pct: int
    agile_chase_buffer_40pct: int
    expected_gross_margin_usd: float


class MarkdownRequest(BaseModel):
    category: str = Field(..., example="Linen Co-ords")
    current_week: int = Field(default=8, ge=1, le=16)
    velocity_change_2w_pct: float = Field(..., example=-12.5)
    search_momentum_4w: float = Field(..., example=-8.0)
    social_momentum_4w: float = Field(..., example=-10.2)
    current_inventory_units: int = Field(default=4000)


class MarkdownResponse(BaseModel):
    category: str
    alert_level: str
    recommended_markdown_pct: float
    recommended_action: str
    effective_selling_price_usd: float
    price_elasticity: float


# --- Endpoints ---

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Fashion Inventory & Markdown Decision Support API",
        "version": "1.0.0",
        "author": "Sri-varshan-07",
    }


@app.get("/catalog")
def get_catalog():
    return catalog_df.to_dict(orient="records")


@app.post("/optimize-inventory", response_model=InventoryResponse)
def optimize_inventory(req: InventoryRequest):
    try:
        alloc = inventory_optimizer.calculate_newsvendor_allocation(
            category=req.category,
            predicted_mean=req.predicted_mean_index,
            lower_80=req.lower_80_index,
            upper_80=req.upper_80_index,
            scale_factor=req.scale_factor,
        )
        return alloc
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/evaluate-markdown", response_model=MarkdownResponse)
def evaluate_markdown(req: MarkdownRequest):
    cat_info = catalog_df[catalog_df["category"] == req.category]
    if cat_info.empty:
        raise HTTPException(status_code=404, detail=f"Category '{req.category}' not found.")

    p0 = float(cat_info["retail_price"].iloc[0])
    elasticity = float(cat_info["price_elasticity"].iloc[0])

    # Rule logic
    is_viral_surge = (req.social_momentum_4w > 10.0) or (req.velocity_change_2w_pct > 15.0)
    is_early_decay = (req.velocity_change_2w_pct < -10.0) and (req.search_momentum_4w < -5.0)
    is_severe_decay = (req.velocity_change_2w_pct < -20.0) or (req.search_momentum_4w < -15.0)

    alert_level = "HEALTHY"
    discount = 0.0
    action = "Maintain full price and standard replenishment."

    if is_viral_surge:
        alert_level = "VIRAL_SURGE_ALERT"
        discount = 0.0
        action = "Trigger nearshore agile chase capacity (+25% inventory injection)."
    elif is_severe_decay:
        alert_level = "SEVERE_DECAY_CRITICAL"
        discount = 0.35
        action = "Execute Stage 2 Clearance Markdown (-35%) to salvage gross margin."
    elif is_early_decay:
        alert_level = "EARLY_DECAY_WARNING"
        discount = 0.15
        action = "Initiate Stage 1 Promotional Discount (-15%) to stimulate velocity."

    effective_price = round(p0 * (1.0 - discount), 2)

    return {
        "category": req.category,
        "alert_level": alert_level,
        "recommended_markdown_pct": discount * 100.0,
        "recommended_action": action,
        "effective_selling_price_usd": effective_price,
        "price_elasticity": elasticity,
    }
