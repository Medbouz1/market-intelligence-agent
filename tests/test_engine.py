import copy
import json
import unittest
from pathlib import Path

from market_intelligence.engine import validate, build_report, portfolio_analysis

DEMO = json.loads((Path(__file__).parent.parent / "examples/demo_snapshot.json").read_text(encoding="utf-8"))


class TestMarketIntelligence(unittest.TestCase):
    def test_demo(self):
        out = build_report(DEMO)
        self.assertTrue(out["synthetic"])
        self.assertFalse(out["orders_enabled"])
        self.assertEqual(out["portfolio"]["status"], "inaccessible")

    def test_no_future_prices(self):
        bad = copy.deepcopy(DEMO)
        bad["markets"][0]["asof"] = "2026-11-18T01:00:00+01:00"
        with self.assertRaisesRegex(ValueError, "après cutoff"):
            validate(bad)

    def test_no_unknown_price_sources(self):
        bad = copy.deepcopy(DEMO)
        bad["markets"][0]["source_id"] = "ABSENT"
        with self.assertRaisesRegex(ValueError, "Source ou heure absente"):
            validate(bad)

    def test_no_nav_when_portfolio_inaccessible(self):
        bad = copy.deepcopy(DEMO)
        bad["portfolio"]["nav"] = 123
        with self.assertRaisesRegex(ValueError, "inaccessible"):
            validate(bad)

    def test_weights(self):
        out = portfolio_analysis({"status":"verified", "nav":1000, "cash":100,
             "asof":"2026-11-16T07:00:00+01:00",
             "positions":[{"ticker":"DEMO","quantity":1,"market_value":850,"currency":"USD","sector":"Technology"}]})
        self.assertEqual(out["positions"][0]["weight_pct"], 85)
        self.assertEqual(out["reconciliation_difference"], 50)
        self.assertTrue(out["warnings"])

    def test_fact_needs_source(self):
        bad = copy.deepcopy(DEMO)
        bad["summary"][0]["source_ids"] = []
        with self.assertRaisesRegex(ValueError, "sans source"):
            validate(bad)


if __name__ == "__main__":
    unittest.main()
