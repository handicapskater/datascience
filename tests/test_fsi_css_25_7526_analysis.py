from __future__ import annotations

import unittest
from pathlib import Path

from scripts.analyze_fsi_css_25_7526 import (
    VEHICLE_FEATURES,
    WALKING_FEATURES,
    fsi_from_vector,
    normalized_vector,
    read_csv,
    row_by,
    validate_filed_ratios,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = REPO_ROOT / "legal/cases/25-7526"
TABLES = CASE_DIR / "outputs/exhibit_a_filed_2026-06-04/tables"


class FsiCssCaseAnalysisTest(unittest.TestCase):
    def test_filed_ratios_reproduce_exhibit_a_values(self) -> None:
        validate_filed_ratios(
            read_csv(TABLES / "walking_vs_mall_pt_ratios.csv"),
            read_csv(TABLES / "paratransit_vehicle_ratios.csv"),
        )

    def test_walking_fsi_uses_mall_pt_reference(self) -> None:
        rows = read_csv(TABLES / "kubios_walk_vs_mall_pt_summary.csv")
        walking = row_by(rows, "analysis_group", "Walking")
        mall_pt = row_by(rows, "analysis_group", "Mall/PT controlled skating")

        walking_fsi = fsi_from_vector(normalized_vector(walking, mall_pt, WALKING_FEATURES))
        mall_pt_fsi = fsi_from_vector(normalized_vector(mall_pt, mall_pt, WALKING_FEATURES))

        self.assertAlmostEqual(mall_pt_fsi, 1.0, places=4)
        self.assertAlmostEqual(walking_fsi, 1.3981, places=4)
        self.assertGreater(walking_fsi, mall_pt_fsi)

    def test_vehicle_fsi_uses_sedan_reference(self) -> None:
        rows = read_csv(TABLES / "kubios_paratransit_vehicle_summary.csv")
        sedan = row_by(rows, "analysis_group", "ParaTransit sedan")
        bus = row_by(rows, "analysis_group", "ParaTransit bus/cutaway")
        van = row_by(rows, "analysis_group", "ParaTransit van")

        sedan_fsi = fsi_from_vector(normalized_vector(sedan, sedan, VEHICLE_FEATURES))
        bus_fsi = fsi_from_vector(normalized_vector(bus, sedan, VEHICLE_FEATURES))
        van_fsi = fsi_from_vector(normalized_vector(van, sedan, VEHICLE_FEATURES))

        self.assertAlmostEqual(sedan_fsi, 1.0, places=4)
        self.assertAlmostEqual(bus_fsi, 1.5662, places=4)
        self.assertAlmostEqual(van_fsi, 1.4858, places=4)
        self.assertGreater(bus_fsi, sedan_fsi)
        self.assertGreater(van_fsi, sedan_fsi)


if __name__ == "__main__":
    unittest.main()
