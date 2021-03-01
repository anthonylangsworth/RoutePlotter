import requests
from typing import List, Tuple, Dict, Iterable, Any
import gzip
import json
import math
import itertools
import multiprocessing
import cProfile
import functools

import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np


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


def total_distance(route: iter) -> float:
    total_distance = 0
    previous_system = None
    for system in route:
        if previous_system:
            total_distance += calc_distance(
                (system["coords"]["x"], system["coords"]["y"], system["coords"]["x"]),
                (previous_system["coords"]["x"], previous_system["coords"]["y"], previous_system["coords"]["x"]))
        previous_system = system
    return total_distance


def add_distance_to_route(route: List[Dict]):
    return (get_system_names(route), total_distance(route))


def permute(head: Any, items: iter) -> iter:
    """
    Split permutation by the first element, a quick and dirty way of parallelizing the work.
    """
    for permutation in itertools.permutations(itertools.filterfalse(lambda x: x == head, items)):
        yield (head,) + permutation


def get_system_names(route: List[Dict]) -> List[str]:
    return [system["name"] for system in route]


def remove_reverse_routes(routes: List[List[Dict]]) -> List[List[Dict]]:
    result = []
    result_reversed_system_names = set()
    for route in routes:
        system_names = get_system_names(route)
        if not "\t".join(system_names) in result_reversed_system_names:
            result.append(route)
            result_reversed_system_names.add("\t".join(system_names[::-1]))
    return result


def calc_shortest_route(head: Dict, systems: Iterable[Dict]) -> Tuple[Dict, float]:
    shortest_route = None
    for route in permute(head, systems):
        distance = total_distance(route)
        if not shortest_route or distance < shortest_route[1]:
            shortest_route = (route, distance)
    return shortest_route


def calc_shortest_route_brute_force(systems: Iterable[Dict]) -> Tuple[Dict, float]:
    with multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1) as pool:
        routes_with_distance = pool.map(functools.partial(calc_shortest_route, systems=systems), systems)
    return functools.reduce(lambda x, y: x if x[1] < y[1] else y, routes_with_distance)


def calc_distances(systems: Iterable[Dict]) -> Iterable[Tuple[int, int, float]]:
    for i in range(len(systems)):
        for j in range(len(systems)):
            if i != j:
                yield (i, j, calc_distance(
                    (systems[i]["coords"]["x"], systems[i]["coords"]["y"], systems[i]["coords"]["z"]),
                    (systems[j]["coords"]["x"], systems[j]["coords"]["y"], systems[j]["coords"]["z"])))


def calc_shortest_route_mlrose(systems: Iterable[Dict]) -> Tuple[Dict, float]:
    # See https://mlrose.readthedocs.io/en/stable/source/tutorial2.html#
    fitness_distances = mlrose.TravellingSales(distances=calc_distances(systems))
    problem_fit = mlrose.TSPOpt(length=len(systems), fitness_fn=fitness_distances, maximize=False)
    best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=20, max_attempts=20)
    return ([systems[index] for index in best_state], best_fitness)


def print_results(description: str, route: List[Dict], distance: float):
    print(f"{ description }: {' -> '.join(get_system_names(route))}: {distance} LY")


def find_longest_jump(route: List[Dict]) -> Tuple[Dict, Dict, float]:
    longest_jump = None
    previous_system = None
    for system in route:
        if previous_system:
            distance = calc_distance(
                (system["coords"]["x"], system["coords"]["y"], system["coords"]["x"]),
                (previous_system["coords"]["x"], previous_system["coords"]["y"], previous_system["coords"]["x"]))
            if not longest_jump or distance > longest_jump[2]:
                longest_jump = (previous_system, system, distance)
        previous_system = system
    return longest_jump


def calc_bubble_run(minor_faction: str):
    systems = get_local_minor_faction_systems(minor_faction)  # Get first X systems as a test with systems[:X:]
    route, distance = calc_shortest_route_mlrose(systems)
    print_results("mlrose", route, distance)

    system1, system2, distance = find_longest_jump(route)
    print(f'Longest jump is {distance} LY between {system1["name"]} and {system2["name"]}')

    # shortest_routes_with_distance_brute_force = calc_shortest_route_brute_force(systems)
    # print_results("brute force", shortest_routes_with_distance_brute_force)


if __name__ == "__main__":
    MINOR_FACTION = "EDA Kunti League"
    calc_bubble_run(MINOR_FACTION)
    # cProfile.run('calc_bubble_run(MINOR_FACTION)')

