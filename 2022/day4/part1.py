import sys
from typing import Tuple


# fucntions for part 1


def right_contains_left(left: Tuple, right: Tuple):
    # left is contained in right
    return (left[0] >= right[0]) and (left[1] <= right[1])


def one_contains_other(left, right):
    return right_contains_left(left, right) or right_contains_left(right, left)


# for part 2
def left_overlaps_right(left, right):
    for i in range(left[0], left[1] + 1):
        if right[0] <= i and i <= right[1]:
            return True
    return False


def any_overlap(left, right):
    return left_overlaps_right(left, right) or left_overlaps_right(right, left)


assert any_overlap([6, 6], [4, 6])
assert not any_overlap([2, 4], [6, 8])
assert not any_overlap([2, 3], [4, 5])


def score(fname):
    num_pairs = 0
    with open(fname, "r") as f:
        pairs = f.readlines()
    for pair in pairs:
        left, right = pair.split(",")
        left = [int(c) for c in left.split("-")]
        right = [int(c) for c in right.split("-")]
        assert len(left) == 2
        assert len(right) == 2
        # if one_contains_other(left, right):
        if any_overlap(left, right):
            num_pairs += 1
    return num_pairs


# assert score("sample.txt") == 2
assert score("sample.txt") == 4, score("sample.txt")


if __name__ == "__main__":
    print(score(sys.argv[1]))
