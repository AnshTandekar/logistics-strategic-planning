import pandas as pd

# Olist public dataset (Kaggle): orders + order items
orders = pd.read_csv(
    "data/olist_orders_dataset.csv",
    parse_dates=["order_purchase_timestamp",
                 "order_delivered_customer_date",
                 "order_estimated_delivery_date"])
items = pd.read_csv("data/olist_order_items_dataset.csv")

# 1. Keep completed deliveries; drop duplicates and missing timestamps
orders = orders[orders["order_status"] == "delivered"].drop_duplicates("order_id")
orders = orders.dropna(subset=["order_delivered_customer_date"]).copy()

# 2. Engineer logistics features
orders["lead_time_days"] = (orders["order_delivered_customer_date"]
                            - orders["order_purchase_timestamp"]).dt.days
orders["late"] = (orders["order_delivered_customer_date"]
                  > orders["order_estimated_delivery_date"])

# 3. Remove impossible / extreme lead times
orders = orders[orders["lead_time_days"].between(0, 60)]

# 4. Attach order value and freight cost
value = (items.groupby("order_id")
              .agg(order_value=("price", "sum"), freight=("freight_value", "sum"))
              .reset_index())
df = orders.merge(value, on="order_id", how="left")

print(df.isna().sum())          # missing-value audit
df.to_csv("data/clean_orders.csv", index=False)
