import pytest
import math
from typing import Tuple

from bubble_runner import calc_distance, permute

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