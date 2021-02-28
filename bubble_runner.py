import requests
from typing import List, Tuple, Dict, Iterable, Any
import gzip
import json
import math
import itertools
import multiprocessing
import cProfile
import functools


def get_all_systems() -> List:
    URL = "https://www.edsm.net/dump/systemsPopulated.json.gz"
    with requests.get(URL) as response:
        response.raise_for_status()
        # TODO: Use a streamed version to save memory
        return json.loads(gzip.decompress(response.content))


def get_local_systems() -> List:
    with open("systemsPopulated.json", "r") as systems_populated:
        return json.loads(systems_populated.read())


def get_systems(minor_faction: str) -> List:
    return [row for row in get_local_systems()
            if "factions" in row and any(
                [faction["name"] for faction in row["factions"] if faction["name"] == minor_faction])]


def get_local_minor_faction_systems(minor_faction: str) -> List:
    with open(f"{minor_faction}.json", "r") as systems_with_minor_faction:
        return json.loads(systems_with_minor_faction.read())


def write_systems(minor_faction: str, systems: List) -> None:
    with open(f"{minor_faction}.json", "w") as file:
        file.write(json.dumps(systems, indent=4))


def calc_distance(point1: Tuple[float, float, float], point2: Tuple[float, float, float]) -> float:
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


def total_distance(route:iter) -> float:
    total_distance = 0
    previous_system = None
    for system in route:
        if previous_system:
            total_distance += calc_distance(
                (system["coords"]["x"], system["coords"]["y"], system["coords"]["x"]),
                (previous_system["coords"]["x"], previous_system["coords"]["y"], previous_system["coords"]["x"]))
        previous_system = system
    return total_distance


def add_distance_to_route(route:List[Dict]):
    return (get_system_names(route), total_distance(route))


def permute(head:Any, items:Iterable[Any]) -> List[Tuple[Any]]:
    """
    Split permutation by the first element, a quick and dirty way of parallelizing the work.
    """
    return [(head,) + permutation for permutation in itertools.permutations([item for item in items if item != head])]


def get_system_names(route:List[Dict]) -> List[str]:
    return [system["name"] for system in route]


def remove_reverse_routes(routes:List[List[Dict]]) -> List[List[Dict]]:
    result = []
    result_reversed_system_names = set()
    for route in routes:
        system_names = get_system_names(route)
        if not "\t".join(system_names) in result_reversed_system_names:
            result.append(route)
            result_reversed_system_names.add("\t".join(system_names[::-1]))
    return result


def calc_bubble_run(minor_faction:str):
    systems = get_local_minor_faction_systems(minor_faction)[:10:] # Get first X systems as a test with systems[:X:]
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        permuted_routes = itertools.chain.from_iterable(pool.map(functools.partial(permute, items=systems), systems))
        permuted_forward_only_routes = remove_reverse_routes(permuted_routes)
        routes_with_distance = pool.map(add_distance_to_route, permuted_forward_only_routes)
    sorted_routes_with_distance = sorted(routes_with_distance, key = lambda route: route[1])

    # for route in sorted_routes_with_distance:
    #     print(f"{', '.join(route[0])}: {route[1]} LY")

    print("Shortest 3 routes:")
    for route in sorted_routes_with_distance[:3:]:
         print(f"{' -> '.join(route[0])}: {route[1]} LY")

    print("Longest 3 routes:")
    for route in sorted_routes_with_distance[-3::]:
         print(f"{' -> '.join(route[0])}: {route[1]} LY")


if __name__ == "__main__":
    MINOR_FACTION = "EDA Kunti League"
    calc_bubble_run(MINOR_FACTION)
    # cProfile.run('calc_bubble_run(MINOR_FACTION)', 'stats')

