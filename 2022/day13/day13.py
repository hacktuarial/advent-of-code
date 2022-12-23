from typing import List


def compare0(left: List, right: List, verbose=False) -> int:
    if verbose:
        print(left, right)
    assert isinstance(left, list)
    assert isinstance(right, list)

    left_empty = len(left) == 0
    right_empty = len(right) == 0
    if left_empty and not right_empty:
        return -1
    elif right_empty and not left_empty:
        return 1
    elif left_empty and right_empty:
        return 0
    else:
        # neither one is empty
        pass
    if isinstance(left[0], int) and isinstance(right[0], int):
        if left[0] < right[0]:
            c = -1
        elif left[0] == right[0]:
            c = 0
        else:
            c = 1
    elif isinstance(left[0], list) and isinstance(right[0], list):
        c = compare0(left[0], right[0], verbose)
    else:
        if isinstance(left[0], int):
            c = compare0(
                [
                    left[0],
                ],
                right[0],
                verbose,
            )
        elif isinstance(right[0], int):
            c = compare0(
                left[0],
                [
                    right[0],
                ],
                verbose,
            )
        else:
            raise ValueError(left, right)
    if c == 0:
        return compare0(left[1:], right[1:], verbose)
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
assert compare0([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [[1], 4], verbose=False) < 0


def part1(fname):
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


def part2(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    entries = [eval(line.strip()) for line in lines if line != "\n"]
    entries.append([[2]])
    entries.append([[6]])
    N = len(entries)
    # bubble sort!
    for i in range(N):
        for j in range(N - i - 1):
            if compare0(entries[j], entries[j + 1]) > 0:
                # swap
                entries[j], entries[j + 1] = entries[j + 1], entries[j]
    print("\n".join([str(e) for e in entries]))
    idx1 = 1 + entries.index([[2]])
    idx2 = 1 + entries.index([[6]])
    return idx1 * idx2


assert part1("sample.txt") == 13
print(part1("input.txt"))
assert part2("sample.txt") == 140, part2("sample.txt")
print(part2("input.txt"))
