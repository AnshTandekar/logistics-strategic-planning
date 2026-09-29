import numpy as np
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

stops = pd.read_csv("data/stops.csv")                 # row 0 = depot
pts = stops[["lat", "lng"]].to_numpy()
# Approximate distance matrix in metres (replace with road distances from OSRM later)
dist = (np.linalg.norm(pts[:, None] - pts[None, :], axis=2) * 111_000).astype(int)
demand = stops["demand_kg"].astype(int).tolist()
NUM_VEHICLES, CAPACITY = 5, 500

manager = pywrapcp.RoutingIndexManager(len(dist), NUM_VEHICLES, 0)
routing = pywrapcp.RoutingModel(manager)

transit = routing.RegisterTransitCallback(
    lambda i, j: int(dist[manager.IndexToNode(i)][manager.IndexToNode(j)]))
routing.SetArcCostEvaluatorOfAllVehicles(transit)

load = routing.RegisterUnaryTransitCallback(lambda i: demand[manager.IndexToNode(i)])
routing.AddDimensionWithVehicleCapacity(load, 0, [CAPACITY] * NUM_VEHICLES, True, "Load")

params = pywrapcp.DefaultRoutingSearchParameters()
params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
params.time_limit.seconds = 10

solution = routing.SolveWithParameters(params)
total_km = 0
for v in range(NUM_VEHICLES):
    idx, route, d = routing.Start(v), [], 0
    while not routing.IsEnd(idx):
        route.append(manager.IndexToNode(idx))
        nxt = solution.Value(routing.NextVar(idx))
        d += routing.GetArcCostForVehicle(idx, nxt, v)
        idx = nxt
    total_km += d / 1000
    print(f"Vehicle {v}: {route + [0]}  ({d/1000:.1f} km)")
print("Total distance (km):", round(total_km, 1))
