# Logistics Strategic Planning: Demand Forecasting, Inventory Control and Route Optimisation

Code accompanying the report *Week 1 Task: Strategic Planning and Data Exploration in Logistics*.

## Scenario
A fictional regional FMCG distributor (one distribution centre, about 1,200 outlets, 45 vehicles) suffers from stock-outs, excess inventory, late deliveries and high delivery cost. This project plans how Python-based data science can address these problems.

## KPIs
OTIF rate, cost per delivery, inventory turnover, fill rate, forecast accuracy (WAPE), fleet utilisation.

## Roadmap
1. Data collection  2. Cleaning and validation  3. Feature engineering  4. Exploratory analysis
5. Predictive modelling  6. Optimisation  7. Evaluation and simulation  8. Insights and decisions

## Repository structure
```
src/
  01_load_clean.py    Load Olist orders, clean, engineer lead time and lateness
  02_kpi_eda.py       Baseline KPIs and exploratory charts
  03_forecast.py      Demand forecasting: Ridge vs gradient boosting (walk-forward, WAPE)
  04_clustering.py    K-Means delivery zones (silhouette score)
  05_routing.py       Capacitated VRP with Google OR-Tools
  06_inventory.py     Safety stock, reorder point, inventory turnover
generate_sample_data.py   Synthetic test data (same column names as Olist)
data/                     Input and intermediate files (ignored by git)
figures/                  Output charts
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Data
**Option A: real data (recommended).** Download the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle and place `olist_orders_dataset.csv` and `olist_order_items_dataset.csv` in `data/`. Check the dataset licence before use.

**Option B: synthetic data (quick test only).**
```bash
python generate_sample_data.py
```
Synthetic data creates the same files plus `data/stops.csv`, so every script runs, but the results are not meaningful.

`data/stops.csv` (columns `stop_id, lat, lng, demand_kg`, row 0 = depot) is used by scripts 04 and 05. It is not part of Olist; build it from your own outlet coordinates or use the synthetic file.

## Run order
Run all commands from the repository root:
```bash
python src/01_load_clean.py
python src/02_kpi_eda.py
python src/03_forecast.py
python src/04_clustering.py
python src/05_routing.py
python src/06_inventory.py
```

## Notes and limitations
- Routing uses straight-line distance as a first approximation; road distances (OSRM) and time windows are planned extensions.
- Forecast features use only past information and validation is time-ordered to avoid data leakage.
- `06_inventory.py` uses illustrative numbers; replace with values from your data.

## References
Dantzig & Ramser (1959); Clarke & Wright (1964); Toth & Vigo (2014); Silver, Pyke & Thomas (2017); Hyndman & Athanasopoulos (2021); Makridakis et al. (2022); Google OR-Tools documentation.

## Author
Ansh Tandekar, Logistics Data Analyst Intern.
