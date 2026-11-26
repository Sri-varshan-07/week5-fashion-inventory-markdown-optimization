"""
Unit tests for Dynamic Markdown & Trend Decay Decision Engine.
"""

import os
import unittest
import pandas as pd
from src.data_loader import load_catalog_metadata, load_forecast_predictions
from src.markdown_engine import DynamicMarkdownEngine


class TestMarkdownEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cls.catalog_df = load_catalog_metadata(base_path=base_dir)
        cls.forecast_df = load_forecast_predictions(base_path=base_dir)
        cls.engine = DynamicMarkdownEngine(cls.catalog_df)

    def test_decay_alerts_generation(self):
        alerts = self.engine.detect_trend_decay_alerts(self.forecast_df)
        self.assertFalse(alerts.empty)
        self.assertIn("alert_level", alerts.columns)
        self.assertIn("recommended_markdown_pct", alerts.columns)

    def test_markdown_revenue_yield_simulation(self):
        sim = self.engine.simulate_markdown_revenue_yield("Linen Co-ords", initial_stock=6000)
        self.assertIn("traditional", sim)
        self.assertIn("algorithmic_dynamic", sim)
        self.assertGreater(sim["algorithmic_dynamic"]["total_revenue"], sim["traditional"]["total_revenue"])
        self.assertGreater(sim["gross_profit_lift_pct"], 0.0)


if __name__ == "__main__":
    unittest.main()
