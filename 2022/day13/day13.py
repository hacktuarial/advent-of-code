from typing import List


def compare0(left: List, right: List) -> int:
    assert isinstance(left, list)
    assert isinstance(right, list)

    if len(left) == 0:
        return -1
    if len(right) == 0:
        return 1
    if isinstance(left[0], int) and isinstance(right[0], int):
        if left[0] < right[0]:
            c = -1
        elif left[0] == right[0]:
            c = 0
        else:
            c = 1
    elif isinstance(left[0], list) and isinstance(right[0], list):
        c = compare0(left[0], right[0])
    else:
        if isinstance(left[0], int):
            c = compare0(
                [
                    left[0],
                ],
                right[0],
            )
        elif isinstance(right[0], int):
            c = compare0(
                left[0],
                [
                    right[0],
                ],
            )
        else:
            raise ValueError(left, right)
    if c == 0:
        return compare0(left[1:], right[1:])
    else:
        return c


assert compare0([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) < 0
assert compare0([[1], [2, 3, 4]], [[1], 4]) < 0
assert compare0([9], [[8, 7, 6]]) > 0
assert compare0([[4, 4], 4, 4], [[4, 4], 4, 4, 4]) < 0
assert compare0([7] * 4, [7] * 3) > 0
assert compare0([], [3]) < 0
assert compare0([[[]]], [[]]) > 0
assert (
    compare0([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9])
    > 0
)


def run(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if line != "\n"]
    index = 1
    total = 0
    while len(lines) > 0:
        left = eval(lines.pop(0))
        right = eval(lines.pop(0))
        if compare0(left, right) < 0:
            total += index
        elif compare0(left, right) == 0:
            raise ValueError(left, right)
        index += 1
    return total


assert run("sample.txt") == 13, run("sample.txt")
print(run("input.txt"))
