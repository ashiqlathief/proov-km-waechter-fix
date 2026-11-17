# analyze.py
# Summary: km_since_service, avg_daily_km and load_factor separate breakdown cars; odometer_km and
# age_years do NOT (means are almost identical in both groups), so old/high-mileage is a myth here.
# The 0-100 risk score weights those three by how strongly each one correlates with breakdowns.
#
# Run: python analyze.py

import pandas as pd

HISTORY_FILE = "fleet_history.csv"
CANDIDATES = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
MIN_CORRELATION = 0.15   # below this a column is treated as noise


def separation(df: pd.DataFrame) -> pd.DataFrame:
    """Compare broke-down vs fine cars, column by column."""
    means = df.groupby("broke_down")[CANDIDATES].mean().T
    means.columns = ["mean_ok", "mean_broke"]
    means["correlation"] = df[CANDIDATES].corrwith(df["broke_down"])
    return means.sort_values("correlation", key=abs, ascending=False)


def risk_scores(df: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Score each car 0-100: weighted average of each factor's rank among all cars."""
    ranks = df[weights.index].rank(pct=True)
    return (ranks * weights).sum(axis=1) / weights.sum() * 100


def main() -> None:
    df = pd.read_csv(HISTORY_FILE)
    table = separation(df)
    print("Do the factors separate cars that broke down from those that did not?")
    print(table.round(3).to_string(), "\n")

    useful = table["correlation"][table["correlation"] >= MIN_CORRELATION]
    print(f"Used in the score: {', '.join(useful.index)}")
    print(f"Ignored (no separation): {', '.join(table.index.difference(useful.index))}\n")

    df["risk"] = risk_scores(df, useful).round(1)
    print("Check: average risk of cars that broke down vs not")
    print(df.groupby("broke_down")["risk"].mean().round(1).to_string(), "\n")

    ranked = df.sort_values("risk", ascending=False)
    print("Cars ranked by risk (highest first):")
    print(ranked[["car_id", "risk", "km_since_service", "avg_daily_km", "load_factor", "broke_down"]]
          .to_string(index=False))


if __name__ == "__main__":
    main()
