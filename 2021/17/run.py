from itertools import product

from joblib import Parallel, delayed

from util import *


@memory.cache()
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
    print(find_highest_style(target=sample, lim=20))
    # print(find_highest_style(target=((175, 227), (-134, -79)), lim=200))
    actual = part2(target=sample, lim=50)
    assert actual == 112, actual
    print(parallel_part2(250))
