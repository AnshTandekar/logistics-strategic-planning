import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# stops.csv: stop_id, lat, lng, demand_kg  (row 0 = depot)
stops = pd.read_csv("data/stops.csv")
customers = stops.iloc[1:].copy()
coords = customers[["lat", "lng"]]

# Choose the number of delivery zones with the silhouette score
best_k, best_score = 2, -1
for k in range(2, 9):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(coords)
    score = silhouette_score(coords, labels)
    if score > best_score:
        best_k, best_score = k, score

customers["zone"] = KMeans(n_clusters=best_k, n_init=10,
                           random_state=42).fit_predict(coords)
print("Best k:", best_k, "| silhouette:", round(best_score, 3))
print(customers.groupby("zone")["demand_kg"].agg(["count", "sum"]))
