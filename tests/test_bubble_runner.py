import pytest
import math
from typing import Tuple, List, Dict

from bubble_runner import calc_distance, permute, remove_reverse_routes, get_system_names


@pytest.mark.parametrize(
    "point1, point2, expected_distance",
    [
        ((1, 1, 1), (1, 1, 1), 0),
        ((1, 1, 1), (2, 2, 2), math.sqrt(3)),
        ((1, 1, 1), (0, 0, 0), math.sqrt(3))
    ]
)
def test_calc_distance(point1: Tuple[float, float, float], point2: Tuple[float, float, float], expected_distance: float):
    assert calc_distance(point1, point2) == expected_distance


@pytest.mark.parametrize(
    "desired_head, items, expected_results",
    [
        (1, [1, 2, 3], [(1, 2, 3), (1, 3, 2)]),
        (2, [1, 2, 3], [(2, 1, 3), (2, 3, 1)]),
    ]
)
def test_permute(desired_head, items, expected_results):
    assert permute(desired_head, items) == expected_results


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
