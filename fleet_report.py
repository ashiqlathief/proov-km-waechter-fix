"""Prints the nightly fleet-health summary for Vossberg Mobility."""

import fleet_utils
from config_loader import load_settings
from km_wachter import SERVICE_INTERVAL_KM, needs_service, wear_percent
from log_util import flush_log, log


def car_wear(car: dict) -> float | None:
    """Return the car's wear in percent, or None if it has no service reading."""
    last = car.get("last_service_km")
    if last is None:
        return None
    return wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list[dict]) -> dict:
    """Count cars, count cars due, and average the wear of cars that have a reading."""
    wears = [w for w in map(car_wear, fleet) if w is not None]
    due = sum(1 for car in fleet if needs_service(car))
    average = sum(wears) / len(wears) if wears else 0.0
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet: list[dict]) -> None:
    """Print the nightly report and write the log."""
    settings = load_settings()
    log(settings.get("report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.1f}%")
    total_km = sum(car["odometer"] for car in fleet)
    # The partner garage in England wants the distance in miles (since 2015).
    miles = fleet_utils.format_number(fleet_utils.km_to_miles(total_km))
    print(f"Fleet distance: {miles} miles")
    flush_log(settings.get("log_file", "km_wachter.log"))
