from typing import List


def compare(left: List, right: List) -> int:
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
        c = compare(left[0], right[0])
    else:
        if isinstance(left[0], int):
            c = compare( [ left[0], ], right[0],)
        elif isinstance(right[0], int):
            c = compare( left[0], [ right[0], ],)
        else:
            raise ValueError(left, right)
    if c == 0:
        return compare(left[1:], right[1:])
    else:
        return c


assert compare([1,1,3,1,1], [1,1,5,1,1]) < 0
assert compare([[1],[2,3,4]], [[1],4]) < 0
assert compare([9], [[8, 7, 6]]) > 0
assert compare([[4,4],4,4] , [[4,4],4,4,4]) < 0
assert compare([7] * 4, [7] * 3) > 0
assert compare([], [3]) < 0
assert compare([[[]]] ,  [[]]) > 0
assert compare([1,[2,[3,[4,[5,6,7]]]],8,9] ,  [1,[2,[3,[4,[5,6,0]]]],8,9]) > 0
