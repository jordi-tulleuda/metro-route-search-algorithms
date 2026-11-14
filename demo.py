"""Small CLI to demonstrate the coursework graph-search algorithms.

Portfolio addition; independent of the original university test runner.
"""
import argparse
from pathlib import Path

from SearchAlgorithm import (
    Astar, Astar_improved, breadth_first_search,
    depth_first_search, uniform_cost_search,
)
from utils import read_cost_table, read_information, read_station_information


ROOT = Path(__file__).resolve().parent
CITIES = {"lyon": "Lyon_smallCity", "barcelona": "Barcelona_City"}
PREFERENCES = {"stops": 0, "time": 1, "distance": 2, "transfers": 3}


def load_map(city):
    folder = ROOT / "CityInformation" / CITIES[city]
    subway = read_station_information(str(folder / "Stations.txt"))
    subway.add_connection(read_cost_table(str(folder / "Time.txt")))
    subway.add_velocity(read_information(str(folder / "InfoVelocity.txt")))
    return subway


def display_station(station_id, subway):
    if station_id == 0:
        return "START (walking connection)"
    if station_id == -1:
        return "DESTINATION (walking connection)"
    entry = subway.stations[int(station_id)]
    return f"{entry['name']} (L{entry['line']}, ID {int(station_id)})"


def main():
    parser = argparse.ArgumentParser(description="Metro graph-search coursework demo")
    parser.add_argument("--city", choices=CITIES, default="lyon")
    parser.add_argument("--algorithm", choices=["dfs", "bfs", "ucs", "astar", "astar-coordinates"], default="astar")
    parser.add_argument("--origin", type=int, help="Origin station ID")
    parser.add_argument("--destination", type=int, help="Destination station ID")
    parser.add_argument("--preference", choices=PREFERENCES, default="time")
    parser.add_argument("--origin-x", type=float)
    parser.add_argument("--origin-y", type=float)
    parser.add_argument("--destination-x", type=float)
    parser.add_argument("--destination-y", type=float)
    parser.add_argument("--list-stations", action="store_true", help="List station IDs and names")
    args = parser.parse_args()
    subway = load_map(args.city)

    if args.list_stations:
        print(f"{args.city.title()} dataset: {len(subway.stations)} stations")
        for station_id, data in subway.stations.items():
            print(f"  {station_id:>2}: {data['name']} (L{data['line']})")
        return

    if args.algorithm == "astar-coordinates":
        coords = [args.origin_x, args.origin_y, args.destination_x, args.destination_y]
        if any(x is None for x in coords):
            parser.error("astar-coordinates requires --origin-x, --origin-y, --destination-x, --destination-y")
        origin, destination = (args.origin_x, args.origin_y), (args.destination_x, args.destination_y)
        route = Astar_improved(origin, destination, subway)
    else:
        if args.origin is None or args.destination is None:
            parser.error("--origin and --destination are required for station-based algorithms")
        for station in (args.origin, args.destination):
            if station not in subway.stations:
                parser.error(f"Station ID {station} not found in the {args.city} dataset")
        if args.algorithm == "dfs":
            route = depth_first_search(args.origin, args.destination, subway)
        elif args.algorithm == "bfs":
            route = breadth_first_search(args.origin, args.destination, subway)
        elif args.algorithm == "ucs":
            route = uniform_cost_search(args.origin, args.destination, subway, PREFERENCES[args.preference])
        else:
            route = Astar(args.origin, args.destination, subway, PREFERENCES[args.preference])

    if route is None:
        print("No route found")
        return

    print(f"Dataset: {args.city}")
    print(f"Algorithm: {args.algorithm}")
    if args.algorithm in ("ucs", "astar"):
        print(f"Optimization criterion: {args.preference}")
    if args.algorithm == "astar-coordinates":
        print("Optimization criterion: time (walking + metro)")
    print("Station IDs:", [int(id) for id in route.route])
    for number, station_id in enumerate(route.route, start=1):
        print(f"  {number}. {display_station(station_id, subway)}")
    if args.algorithm in ("ucs", "astar", "astar-coordinates"):
        print(f"Accumulated cost (g): {route.g:.3f}")
        if args.algorithm in ("astar", "astar-coordinates"):
            print(f"A* evaluation (f): {route.f:.3f}")


if __name__ == "__main__":
    main()
