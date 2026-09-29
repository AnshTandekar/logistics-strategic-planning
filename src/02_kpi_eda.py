import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean_orders.csv", parse_dates=["order_purchase_timestamp"])

# Baseline KPIs
kpis = {
    "On-time delivery rate (%)": 100 * (1 - df["late"].mean()),
    "Average lead time (days)": df["lead_time_days"].mean(),
    "Freight as % of order value": 100 * df["freight"].sum() / df["order_value"].sum(),
}
print(pd.Series(kpis).round(2))

# Demand pattern and lateness by weekday
weekly = df.set_index("order_purchase_timestamp").resample("W")["order_id"].count()
weekly.plot(title="Weekly order volume")
plt.savefig("figures/weekly_volume.png", dpi=150, bbox_inches="tight")

late_by_day = df.groupby(df["order_purchase_timestamp"].dt.dayofweek)["late"].mean()
print(late_by_day.round(3))
