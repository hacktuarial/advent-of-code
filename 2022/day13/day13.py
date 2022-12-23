from typing import List

def compare(left: List, right: List):
    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right, ])

    assert isinstance(left, list)
    assert isinstance(right, list)

    if len(right) * len(left) == 0:
        return True
    if len(right) == 0:
        return True
    if isinstance(left[0], int) and isinstance(right[0], int):
        return left[0] < right[0] and compare(left[1:], right[1:])
    elif isinstance(left[0], list) and isinstance(right[0], list):
        return compare(left[0], right[0]) and compare(left[1:], right[1:])
    else:
        raise ValueError(left, right)


assert not compare([7] * 4, [7] * 3)
assert compare([2, 3, 4], [4])
assert compare([1,1,3,1,1], [1,1,5,1,1])
assert compare([[1],[2,3,4]], [[1],4])
