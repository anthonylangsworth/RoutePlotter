import functools
from typing import List, Tuple

import star_systems

PRO_INFLUENCE_THRESHOLD = 0.5
ANTI_INFLUENCE_THRESHOLD = 0.6


def is_influence_below(system: object, minor_faction_name: str, anti_influence_threshold: float) -> bool:
    minor_faction = next(filter(lambda factions: factions["name"] == minor_faction_name, system["factions"]), None)
    return minor_faction["influence"] > anti_influence_threshold if minor_faction else False


def get_anti(systems: List[object], minor_faction_name: str, anti_influence_threshold: float) -> List[Tuple[str, float]]:
    return filter(functools.partial(is_influence_below, ))


def generate_report(minor_faction_name: str):
    systems = list(star_systems.get_systems(functools.partial(star_systems.matches_minor_faction, minor_faction_name)))
    print("Anti")
    print(get_anti(systems, minor_faction_name, ANTI_INFLUENCE_THRESHOLD))


if __name__ == "__main__":
    MINOR_FACTION = "EDA Kunti League"
    generate_report(MINOR_FACTION)
    # cProfile.run('calc_bubble_run(MINOR_FACTION)')
