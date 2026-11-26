"""
Unit tests for Prescriptive Inventory Optimization Engine.
"""

import os
import unittest
import pandas as pd
import numpy as np

from src.data_loader import load_catalog_metadata
from src.inventory_engine import FashionInventoryOptimizer


class TestInventoryEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cls.catalog_df = load_catalog_metadata(base_path=base_dir)
        cls.optimizer = FashionInventoryOptimizer(cls.catalog_df)

    def test_newsvendor_critical_fractile(self):
        # Oversized Blazers: Retail 180, Cost 65, Salvage 45
        # Cu = 180 - 65 = 115
        # Co = 65 - 45 = 20
        # fractile = 115 / (115 + 20) = 115 / 135 = 0.85185
        alloc = self.optimizer.calculate_newsvendor_allocation(
            category="Oversized Blazers",
            predicted_mean=55.0,
            lower_80=50.0,
            upper_80=60.0,
            scale_factor=100.0,
        )
        self.assertAlmostEqual(alloc["critical_fractile"], 0.8519, places=3)
        self.assertGreater(alloc["optimal_order_quantity_Q"], alloc["expected_demand_units"])
        self.assertEqual(alloc["pre_commitment_overseas_60pct"], int(0.60 * alloc["expected_demand_units"]))

    def test_safety_stock_calculation(self):
        ss_info = self.optimizer.compute_safety_stock_and_rop(
            category="Retro Sportswear",
            weekly_demand_mean=500.0,
            weekly_demand_std=60.0,
            lead_time_weeks=4,
            service_level=0.90,
        )
        self.assertGreater(ss_info["safety_stock_units"], 0)
        self.assertGreater(ss_info["reorder_point_units"], ss_info["lead_time_demand_units"])


if __name__ == "__main__":
    unittest.main()
