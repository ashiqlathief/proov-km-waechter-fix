# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_survives_car_with_no_reading():
    # VOS-7788 has no "last_service_km". The report must not crash and must not count it as due.
    fleet = SAMPLE + [{"id": "VOS-7788", "odometer": 92000}]
    summary = fleet_summary(fleet)
    assert summary["count"] == 3
    assert summary["due"] == 1
