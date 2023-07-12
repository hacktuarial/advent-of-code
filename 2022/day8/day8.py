import logging

logging.basicConfig(level=logging.DEBUG)


def count_left(mat, i, j):
    k = 1
    for k in range(1, j + 1):
        if mat[i][j - k] >= mat[i][j]:
            break
    return k


def count_right(mat, i, j):
    k = 1
    n_cols = len(mat[0]) - 1
    for k in range(1, n_cols - j + 1):
        if mat[i][j + k] >= mat[i][j]:
            break
    return k


def count_up(mat, i, j):
    k = 1
    for k in range(1, i + 1):
        if mat[i - k][j] >= mat[i][j]:
            break
    return k


def count_down(mat, i, j):
    k = 1
    n_rows = len(mat)
    for k in range(1, n_rows - i):
        if mat[i + k][j] >= mat[i][j]:
            break
    return k


def visible_from_left(mat, i, j):
    for k in range(0, j):
        if mat[i][k] >= mat[i][j]:
            return False
    return True


def visible_from_right(mat, i, j):
    for k in range(j + 1, len(mat[0])):
        if mat[i][k] >= mat[i][j]:
            return False
    return True


def visible_from_top(mat, i, j):
    for k in range(0, i):
        if mat[k][j] >= mat[i][j]:
            return False
    return True


def visible_from_bottom(mat, i, j):
    for k in range(i + 1, len(mat)):
        if mat[k][j] >= mat[i][j]:
            return False
    return True


def is_visible(mat, i, j):
    return (
        visible_from_left(mat, i, j)
        or visible_from_right(mat, i, j)
        or visible_from_top(mat, i, j)
        or visible_from_bottom(mat, i, j)
    )


def read(fname):
    with open(fname, "r") as f:
        mat = f.readlines()
    mat = [[int(i) for i in line.strip()] for line in mat]
    return mat


def scenic_score(mat, i, j):
    # first row or column
    if i * j == 0:
        return 0
    # last row or column
    if i == len(mat) - 1 or j == len(mat[0]) - 1:
        return 0
    return (
        count_left(mat, i, j)
        * count_right(mat, i, j)
        * count_up(mat, i, j)
        * count_down(mat, i, j)
    )


def max_scenic_score(mat):
    max_score = 0
    for i in range(1, len(mat) - 1):
        for j in range(1, len(mat[0]) - 1):
            score = scenic_score(mat, i, j)
            if score > max_score:
                max_score = score
                logging.debug("Found new max score of %d at (%d, %d)", max_score, i, j)
    return max_score


if __name__ == "__main__":
    mat = read("sample.txt")
    assert is_visible(mat, 1, 2)
    for i in range(5):
        assert is_visible(mat, i, 0)
        assert is_visible(mat, 0, i)
    n = sum(is_visible(mat, i, j) for i in range(len(mat)) for j in range(len(mat[0])))
    assert n == 21, n

    # part 2
    assert count_left(mat, 1, 2) == 1
    assert count_left(mat, 0, 3) == 3
    assert count_right(mat, 1, 2) == 2
    assert count_up(mat, 1, 2) == 1
    assert count_down(mat, 1, 2) == 2
    assert scenic_score(mat, 1, 2) == 4
    assert count_left(mat, 3, 2) == 2
    assert count_right(mat, 3, 2) == 2
    assert count_up(mat, 3, 2) == 2
    assert count_down(mat, 3, 2) == 1
    assert max_scenic_score(mat) == 8, max_scenic_score(mat)

    mat1 = read("input.txt")
    n = sum(
        is_visible(mat1, i, j) for i in range(len(mat1)) for j in range(len(mat1[0]))
    )
    logging.info("part1 = %d", n)

    logging.info("part2 = %d", max_scenic_score(mat1))
