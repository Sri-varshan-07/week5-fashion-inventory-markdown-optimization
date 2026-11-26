"""
Unit tests for FastAPI Decision Support Endpoints (Direct function execution).
"""

import unittest
from src.api import (
    health_check,
    get_catalog,
    optimize_inventory,
    evaluate_markdown,
    InventoryRequest,
    MarkdownRequest,
)


class TestAPI(unittest.TestCase):

    def test_health_endpoint(self):
        resp = health_check()
        self.assertEqual(resp["status"], "healthy")
        self.assertEqual(resp["author"], "Sri-varshan-07")

    def test_catalog_endpoint(self):
        resp = get_catalog()
        self.assertGreaterEqual(len(resp), 4)
        categories = [item["category"] for item in resp]
        self.assertIn("Oversized Blazers", categories)
        self.assertIn("Retro Sportswear", categories)

    def test_optimize_inventory_endpoint(self):
        req = InventoryRequest(
            category="Oversized Blazers",
            predicted_mean_index=55.0,
            lower_80_index=50.0,
            upper_80_index=60.0,
            scale_factor=100.0,
        )
        resp = optimize_inventory(req)
        self.assertEqual(resp["category"], "Oversized Blazers")
        self.assertGreater(resp["optimal_order_quantity_Q"], 5000)
        self.assertEqual(resp["pre_commitment_overseas_60pct"], int(0.60 * resp["expected_demand_units"]))

    def test_evaluate_markdown_endpoint(self):
        req = MarkdownRequest(
            category="Linen Co-ords",
            current_week=8,
            velocity_change_2w_pct=-15.0,
            search_momentum_4w=-8.0,
            social_momentum_4w=-5.0,
            current_inventory_units=4000,
        )
        resp = evaluate_markdown(req)
        self.assertEqual(resp["category"], "Linen Co-ords")
        self.assertEqual(resp["alert_level"], "EARLY_DECAY_WARNING")
        self.assertEqual(resp["recommended_markdown_pct"], 15.0)


if __name__ == "__main__":
    unittest.main()
