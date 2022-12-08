import logging

logging.basicConfig(level=logging.INFO)


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


if __name__ == "__main__":
    mat = read("sample.txt")
    assert is_visible(mat, 1, 2)
    for i in range(5):
        assert is_visible(mat, i, 0)
        assert is_visible(mat, 0, i)
    n = sum(is_visible(mat, i, j) for i in range(len(mat)) for j in range(len(mat[0])))
    assert n == 21, n
    del mat

    mat1 = read("input.txt")
    n = sum(is_visible(mat1, i, j) for i in range(len(mat1)) for j in range(len(mat1[0])))
    logging.info("part1 = %d", n)
