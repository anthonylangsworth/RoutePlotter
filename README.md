# Introduction

This was originally meant to be the seed of another EDMC plug-in. The plug-in's initial task was to download the star systems with a given minor faction's presence then determine the shortest route.

It soon become clear that, for any non-trivial number of star systems (n > 5), this would take too long. There are also other potential uses for a tool that can plot the shortest route between stars, such as community goals.

Therefore, the focus moved from creating an EDMC plug-in to plotting routes between stars in the most efficient way. It was also a good opportunity to large about Python's multiprocessing library and optimizations (e.g. using iterators and a string lookup in a `set` instead of a `list` lookup in a `list`).

A better solution was to use a genetic algorithm, e.g. mlrose. This approximated the output very quickly.

# Backlog
1. Create a new version of itertools.permutations to create a "triangle" output for the brute force version.
2. Rename to "route plotter" or similar?
