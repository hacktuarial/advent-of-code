from itertools import product

from joblib import Parallel, delayed

from util import *


def helper(xy):
    target = ((175, 227), (-134, -79))
    return test_probe(*xy, target)


def parallel_part2(lim):
    combos = product(range(-lim, lim), range(-lim, lim))
    results = Parallel(n_jobs=6)(delayed(helper)(xy) for xy in combos)
    return sum(results)


if __name__ == "__main__":
    sample = ((20, 30), (-10, -5))
    assert test_probe(6, 0, sample)
    assert test_probe(7, -1, sample)
    full = ((175, 227), (-134, -79))
    assert 45 == find_highest_style(target=sample, lim=20)[1]
    # assert 8911 == find_highest_style(target=full, lim=200)
    assert part2(target=sample, lim=50) == 112
    print(parallel_part2(230))  # answer should be more than 4400
