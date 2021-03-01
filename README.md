# Introduction

This was originally meant to be the seed of another EDMC plug-in. The plug-in's initial task was to download the star systems with a given minor faction's presence then determine the shortest route. 

It soon become clear that, for any non-trivial number of star systems (n > 5), this would take too long. There are also other potential uses for a tool that can plot the shortest route between stars, such as community goals.

Therefore, the focus moved from creating an EDMC plug-in to plotting routes between stars in the most efficient way. It was also a good opportunity to large about Python's multiprocessing library and optimizations (e.g. using a string lookup in a `set` instead of a `list` lookup in a `list`).

# Backlog
1. Swap the final sort to a reduce, creating a map/reduce pattern.
2. Stop substituting systems with the system name until the end. There could be additional uses for the full system data, e.g. determining the longest jump to help commanders engineer their ship's FSDs for jump range.
3. Create a new version of itertools.permutations to create a "triangle" output.
4. Rename to "route plotter" or similar?
