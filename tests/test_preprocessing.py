import unittest
import pandas as pd
from utils.prep import normalize_sheet, aggregate_daily
from utils.schema import SOURCE_HIST, SOURCE_LIVE


class TestPrep(unittest.TestCase):
    def sample(self):
        return pd.DataFrame([
            dict(source=SOURCE_HIST, region_code="11", region="Île-de-France",
                 observation_utc="2025-01-01T00:00:00+00:00", consumption_mw=100,
                 nuclear_mw=20, wind_mw=10, solar_mw=10, hydro_mw=10, thermal_mw=10, bioenergy_mw=10),
            dict(source=SOURCE_LIVE, region_code="11", region="Île-de-France",
                 observation_utc="2025-01-01T00:15:00+00:00", consumption_mw=90),
            dict(source=SOURCE_HIST, region_code="11", region="Île-de-France",
                 observation_utc="2025-01-01T00:00:00+00:00", consumption_mw=100),
        ])

    def test_deduplication_and_historical_precedence(self):
        frame, q = normalize_sheet(self.sample())
        self.assertEqual(len(frame), 1)
        self.assertEqual(q["superseded_live_rows"], 1)
        self.assertAlmostEqual(frame.iloc[0].consumption_mwh, 50.0)

    def test_negative_demand_kept_as_missing(self):
        frame = self.sample().iloc[:1].copy()
        frame.loc[frame.index[0], "consumption_mw"] = -9
        result, _ = normalize_sheet(frame)
        self.assertTrue(pd.isna(result.iloc[0].consumption_mw))

    def test_daily_energy(self):
        frame, _ = normalize_sheet(self.sample().iloc[:1])
        d = aggregate_daily(frame)
        self.assertAlmostEqual(d.iloc[0].consumption_mwh, 50)
        self.assertEqual(d.iloc[0].readings, 1)


if __name__ == "__main__":
    unittest.main()
