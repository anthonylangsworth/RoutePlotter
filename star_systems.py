import requests
from typing import List, Dict, Callable
import gzip
import json


def download_populated_systems() -> List:
    # To download systemsPopulated.json (in a Un*x prompt):
    # wget https://www.edsm.net/dump/systemsPopulated.json.gz
    # gunzip systemsPopulated.json.gz
    URL = "https://www.edsm.net/dump/systemsPopulated.json.gz"
    with requests.get(URL) as response:
        response.raise_for_status()
        # TODO: Use a streamed version to save memory
        return json.loads(gzip.decompress(response.content))


def get_populated_systems() -> Dict:
    with open("systemsPopulated.json", "r") as systems_populated:
        return json.loads(systems_populated.read())


def get_systems(predicate: Callable[[Dict], bool]) -> iter:
    for row in get_populated_systems():
        if predicate(row):
            yield row


def matches_minor_faction(minor_faction: str, row: Dict) -> bool:
    return "factions" in row and any([faction["name"] == minor_faction and faction["influence"] > 0 for faction in row["factions"]])


def get_local_minor_faction_systems(minor_faction: str) -> List:
    with open(f"{minor_faction}.json", "r") as systems_with_minor_faction:
        return json.loads(systems_with_minor_faction.read())


def write_systems(minor_faction: str, systems: List[Dict]) -> None:
    with open(f"{minor_faction}.json", "w") as file:
        file.write(json.dumps(systems, indent=4))
