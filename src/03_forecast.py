import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit

df = pd.read_csv("data/clean_orders.csv", parse_dates=["order_purchase_timestamp"])
daily = (df.set_index("order_purchase_timestamp")
           .resample("D")["order_id"].count().rename("demand").to_frame())

# Calendar + lag features (only past information, so no data leakage)
daily["dow"] = daily.index.dayofweek
for lag in (1, 7, 14):
    daily[f"lag_{lag}"] = daily["demand"].shift(lag)
daily["roll7"] = daily["demand"].shift(1).rolling(7).mean()
daily = daily.dropna()

X, y = daily.drop(columns="demand"), daily["demand"]
wape = lambda a, p: np.abs(a - p).sum() / a.sum()

models = {"Ridge (baseline)": Ridge(alpha=1.0),
          "Gradient boosting": GradientBoostingRegressor(random_state=42)}
for name, model in models.items():
    scores = []
    for train, test in TimeSeriesSplit(n_splits=5).split(X):   # walk-forward validation
        model.fit(X.iloc[train], y.iloc[train])
        scores.append(wape(y.iloc[test], model.predict(X.iloc[test])))
    print(f"{name}: WAPE = {np.mean(scores):.3f}")
