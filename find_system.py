import star_systems

if __name__ == "__main__":
    SORTED_NAME = sorted("TFZIRQRL".lower())
    matching_star_systems = list(star_systems.get_systems(lambda x: sorted(x["name"].lower()) == SORTED_NAME))
    for matching_star_system in matching_star_systems:
        print(matching_star_system["name"], "\n")
