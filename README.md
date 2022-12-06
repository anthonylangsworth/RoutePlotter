# Route Plotter

## Introduction

**Route Plotter** is a small Python program that calculates the shortest route to visit all star systems where a minor faction in the **Elite Dangerous** galaxy is present. Visiting each star system in-game while running a tool like [Elite Dangerous Market Connector (EDMC)](https://edcodex.info/?m=tools&entry=150) ensures the data in third-party tools like [Inara](https://inara.cz/elite/news/), [EDSM](https://edsm.net) and [elitebgs.app](https://elitebgs.app/) is up-to-date. This helps players supporting a minor faction determine whether work is required to support, protect or expand their minor faction.

This problem is a traditional "travelling salesman" problem, solved using a genetic algorithm with the [MLROSE](https://mlrose.readthedocs.io/en/stable/) library.

## Use

In a Linux prompt (using [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) on Windows):
1. Download the files, such as by a `git clone` of this repository's URL.
2. Navigate to the folder containing the files from this project.
3. Run `pip install -r requirements.txt` to download dependencies. This only needs to be run the first time. After that, the dependences are present.
4. Run `wget https://www.edsm.net/dump/systemsPopulated.json.gz` to download the latest data on populated star systems from [EDSM](https://edsm.net).
5. Run `gunzip systemsPopulated.json.gz` to decompress the downloaded file.
6. (Optional) Change the name of the minor faction in `MINOR_FACTION` around line 135. It defaults to my minor faction but yours is likely different.
7. Run `python bubble_runner.py`. It outputs the following to the console:
    1. The route. Start at any system then follow the jump sequence.
    2. The longest jump required. A ship that can jump at least this far can do the route in a single jump per step. 

## License

See [LICENSE](LICENSE).
