import json
from functools import lru_cache

import numpy as np


def absolute_distance(steps):
    return abs(steps)


@lru_cache
def greater_distance(steps):
    return sum(range(steps + 1))


assert greater_distance(2) == 1 + 2
assert greater_distance(3) == 1 + 2 + 3


def total_cost(positions, destination, cost_fn, min_cost):
    total = 0
    for i in range(len(positions)):
        total += cost_fn(abs(positions[i] - destination))
        if total >= min_cost:
            break
    return total


def find_min(positions, cost_fn):
    min_cost = np.inf
    for dest in range(max(positions)):
        cost = total_cost(positions, dest, cost_fn, min_cost)
        min_cost = min(min_cost, cost)
    return min_cost


if __name__ == "__main__":
    sample = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert find_min(sample, absolute_distance) == 37
    assert find_min(sample, greater_distance) == 168
    with open("input.json", "r") as f:
        full = json.load(f)
    print(find_min(full, greater_distance))
