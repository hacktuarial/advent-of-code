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
    print(find_highest_style(target=((20, 30), (-10, -5)), lim=20))
    # print(find_highest_style(target=((175, 227), (-134, -79)), lim=200))
    # print(part2(target=((175, 227), (-134, -79)), lim=500))
    print(parallel_part2(500))
