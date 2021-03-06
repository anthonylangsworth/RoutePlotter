import pytest
import math
from typing import Tuple, List, Dict, Iterable

from bubble_runner import calc_distance, permute, remove_reverse_routes, get_system_names, calc_shortest_route, calc_distances, get_local_minor_faction_systems


@pytest.mark.parametrize(
    "point1, point2, expected_distance",
    [
        ((1, 1, 1), (1, 1, 1), 0),
        ((1, 1, 1), (2, 2, 2), math.sqrt(3)),
        ((1, 1, 1), (0, 0, 0), math.sqrt(3))
    ]
)
def test_calc_distance_basic(point1: Tuple[float, float, float], point2: Tuple[float, float, float], expected_distance: float):
    assert calc_distance(point1, point2) == expected_distance


@pytest.mark.parametrize(
    "system1_name, system2_name, expected_distance",
    [
        ("Herci", "LTT 2412", 34.64),
        ("Herci", "Antai", 30.27), # Might be 30.30 in-game. Hmmm.
        ("Antai", "Anukan", 14.61),
        ("Antai", "Arun", 11.94),
        ("Antai", "Wuy jugun", 21.62)
    ]
)
def test_calc_distance_in_game(system1_name: Dict, system2_name: Dict, expected_distance: float):
    systems = get_local_minor_faction_systems("EDA Kunti League")
    system1 = next(system for system in systems if system["name"] == system1_name)
    system2 = next(system for system in systems if system["name"] == system2_name)
    assert round(calc_distance(
        (system1["coords"]["x"], system1["coords"]["y"], system1["coords"]["z"]),
        (system2["coords"]["x"], system2["coords"]["y"], system2["coords"]["z"])), 2) == expected_distance


@pytest.mark.parametrize(
    "desired_head, items, expected_results",
    [
        (1, [1, 2, 3], [(1, 2, 3), (1, 3, 2)]),
        (2, [1, 2, 3], [(2, 1, 3), (2, 3, 1)]),
    ]
)
def test_permute(desired_head, items, expected_results):
    assert list(permute(desired_head, items)) == expected_results


@pytest.mark.parametrize(
    "route, expected_names",
    [
        ([], []),
        ([{"name": "foo"}], ["foo"]),
        ([{"name": "a", "id": 3}, {"name": "b"}, {"name": "c"}], ["a", "b", "c"]),
    ]
)
def test_get_system_names(route: List, expected_names: List):
    assert get_system_names(route) == expected_names


@pytest.mark.parametrize(
    "routes",
    [
        (),
        (
            [{"name": "a"}, {"name": "b"}, {"name": "c"}],
        ),
        (
            [{"name": "a"}, {"name": "b"}, {"name": "c"}],
            [{"name": "a"}, {"name": "c"}, {"name": "b"}],
        ),
        (
            [{"name": "a"}, {"name": "b"}, {"name": "c"}],
            [{"name": "a"}, {"name": "c"}, {"name": "b"}],
            [{"name": "b"}, {"name": "a"}, {"name": "c"}],
            [{"name": "b"}, {"name": "c"}, {"name": "a"}],
            [{"name": "c"}, {"name": "a"}, {"name": "b"}],
            [{"name": "c"}, {"name": "b"}, {"name": "a"}]
        ),
    ]
)
def test_remove_reverse_routes(routes: List[Dict]):
    result = remove_reverse_routes(routes)
    routes_system_names = [get_system_names(route) for route in routes]
    result_system_names = [get_system_names(route) for route in result]
    result_reversed_system_names = [get_system_names(route)[::-1] for route in result]
    assert len([system_names for system_names in result_system_names if system_names in result_reversed_system_names]) == 0
    assert len([system_names for system_names in routes_system_names if not (system_names in result_system_names or system_names in result_reversed_system_names)]) == 0


@pytest.mark.parametrize(
    "head, systems, expected_shortest_route",
    [
        (
            {"name": "Antai", "coords":{"x": 94.9375, "y": -44.65625, "z": -16.09375}},
            [
                {"name": "Antai", "coords":{"x": 94.9375, "y": -44.65625, "z": -16.09375}},
                {"name": "Wuy jugun", "coords":{"x": 116, "y": -41.875, "z": -12.09375}},
                {"name": "Arun", "coords": {"x": 105.25, "y": -46.625, "z": -10.40625}}
            ],
            (
                ["Antai", "Arun", "Wuy jugun"], 23.813512634832392
            )
        )
    ]
)
def test_calc_shortest_route(head: Dict, systems: Iterable[Dict], expected_shortest_route: Tuple[List[str], float]):
    systems, distance = calc_shortest_route(head, systems)
    assert (get_system_names(systems), distance) == expected_shortest_route


@pytest.mark.parametrize(
    "systems, expected_distances",
    [
        (
            [
                {"name": "Antai", "coords":{"x": 94.9375, "y": -44.65625, "z": -16.09375}},
                {"name": "Wuy jugun", "coords":{"x": 116, "y": -41.875, "z": -12.09375}},
                {"name": "Arun", "coords": {"x": 105.25, "y": -46.625, "z": -10.40625}}
            ],
            (
                [(0, 1, 21.618609062853697), (0, 2, 11.940321983200453), (1, 0, 21.618609062853697), (1, 2, 11.873190651631937), (2, 0, 11.940321983200453), (2, 1, 11.873190651631937)]
            )
        )
    ]
)
def test_calc_distances(systems: Iterable[Dict], expected_distances: Iterable[Tuple[int, int, float]]):
    assert list(calc_distances(systems)) == expected_distances