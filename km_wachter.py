"""KM-Waechter decides when a Vossberg Mobility car needs a service."""

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return how much of the service interval is used up, in percent."""
    return km_since_service / interval * 100


def needs_service(car: dict) -> bool:
    """Return True if the car is worn past the warning threshold.

    A car with no last-service reading is never flagged: its wear is unknown.
    """
    last = car.get("last_service_km")
    if last is None:
        return False
    km_since = car["odometer"] - last
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Print and return the ids of all cars that are due for service."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
