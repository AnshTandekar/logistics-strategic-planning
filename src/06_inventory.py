from scipy.stats import norm

def reorder_point(mean_daily, std_daily, lead_days, service_level=0.95):
    """Reorder point = demand during lead time + safety stock."""
    z = norm.ppf(service_level)
    safety_stock = z * std_daily * lead_days ** 0.5
    return mean_daily * lead_days + safety_stock, safety_stock

def inventory_turnover(cogs, avg_inventory_value):
    return cogs / avg_inventory_value

rop, ss = reorder_point(mean_daily=120, std_daily=25, lead_days=4)
print(f"Safety stock: {ss:.0f} units | Reorder point: {rop:.0f} units")
print("Turnover:", round(inventory_turnover(9_000_000, 1_500_000), 1), "times/year")
