"""Creates SYNTHETIC test data with the same column names as the public Olist files
and a small routing instance. Use it to check that the scripts run end to end.
Replace with the real Olist CSVs (see README) for meaningful results."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
n = 4000
ts = pd.Timestamp("2017-01-01") + pd.to_timedelta(rng.integers(0, 600, n), unit="D")
lead = rng.integers(3, 25, n)

orders = pd.DataFrame({
    "order_id": [f"o{i}" for i in range(n)],
    "customer_id": range(n),
    "order_status": rng.choice(["delivered", "canceled"], n, p=[0.95, 0.05]),
    "order_purchase_timestamp": ts,
    "order_delivered_customer_date": ts + pd.to_timedelta(lead, unit="D"),
    "order_estimated_delivery_date": ts + pd.to_timedelta(rng.integers(8, 25, n), unit="D"),
})
orders.loc[orders.sample(50, random_state=1).index, "order_delivered_customer_date"] = pd.NaT
orders.to_csv("data/olist_orders_dataset.csv", index=False)

pd.DataFrame({"order_id": orders.order_id,
              "price": rng.uniform(20, 300, n),
              "freight_value": rng.uniform(5, 40, n)}
             ).to_csv("data/olist_order_items_dataset.csv", index=False)

stops = pd.DataFrame({"stop_id": range(41),
                      "lat": 19.99 + rng.normal(0, 0.08, 41),
                      "lng": 73.78 + rng.normal(0, 0.08, 41),
                      "demand_kg": rng.integers(20, 90, 41)})
stops.loc[0, "demand_kg"] = 0          # row 0 = depot
stops.to_csv("data/stops.csv", index=False)
print("Synthetic data written to data/")
