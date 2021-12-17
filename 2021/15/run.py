from typing import Tuple

from logzero import logger
from numpy.testing import assert_array_equal
import numpy as np


def read_input(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    matrix = []
    for line in lines:
        line = line.strip()
        row = []
        for x in line:
            row.append(int(x))
        matrix.append(row)
    return np.array(matrix)


def get_neighbors(matrix, vertex):
    row, col = vertex
    neighbors = []
    if row - 1 >= 0:
        neighbors.append((row - 1, col))  # up
    if row + 1 < matrix.shape[0]:
        neighbors.append((row + 1, col))  # down
    if col - 1 >= 0:
        neighbors.append((row, col - 1))  # left
    if col + 1 < matrix.shape[1]:
        neighbors.append((row, col + 1))  # right
    return neighbors


assert set(get_neighbors(np.ones((2, 2)), (0, 0))) == set([(0, 1), (1, 0)])
assert set(get_neighbors(np.ones((3, 3)), (0, 1))) == set([(0, 0), (0, 2), (1, 1)])
assert set(get_neighbors(np.ones((3, 3)), (1, 1))) == set(
    [(0, 1), (1, 0), (1, 2), (2, 1)]
)


def find_min_distance(matrix, known) -> Tuple[int]:
    """Returns the index of the minimum value"""
    min_distance = matrix[:, :]  # copy
    min_distance[known > 0] = np.inf
    return np.unravel_index(min_distance.argmin(), min_distance.shape)


def dijkstra(matrix, start: Tuple, end: Tuple):
    known = np.zeros_like(matrix).astype(bool)
    distances = np.ones(matrix.shape) * np.inf
    for neighbor in get_neighbors(matrix, start):
        # no cost incurred at starting vertex
        distances[neighbor[0], neighbor[1]] = matrix[neighbor[0], neighbor[1]]
    last = start
    while last != end:
        v = find_min_distance(distances, known)
        for neighbor in get_neighbors(matrix, v):
            current_distance = distances[neighbor[0], neighbor[1]]
            new_distance = distances[v[0], v[1]] + matrix[neighbor[0], neighbor[1]]
            distances[neighbor[0], neighbor[1]] = min(current_distance, new_distance)
        last = v
        known[v[0], v[1]] = True
        logger.info("visited %f vertices", known.sum() / (matrix.shape[0] ** 2))
    return distances[end[0], end[1]]


def increment(matrix, n_times):
    if n_times == 0:
        return matrix
    new_matrix = matrix[:, :]
    for i in range(n_times):
        new_matrix = 1 + new_matrix
        new_matrix[new_matrix == 10] = 1
    return new_matrix


mat = read_input("sample.txt")
assert_array_equal(mat, increment(mat, 0))


def expand(matrix):
    dim = matrix.shape[0]
    matrix_out = np.zeros((dim * 5, dim * 5))
    for i in range(5):
        for j in range(5):
            matrix_out[dim * i : dim * (i + 1), dim * j : dim * (j + 1)] = increment(
                matrix, i + j
            )
    return matrix_out


actual = expand(read_input("sample.txt"))
assert actual.shape == (50, 50)
expected = read_input("sample_expanded.txt")
assert (actual == expected).all()


def part1(fname):
    matrix = read_input(fname)
    logger.info(matrix.shape)
    # assuming it's square
    start = (0, 0)
    end = (matrix.shape[0] - 1, matrix.shape[1] - 1)
    cost = dijkstra(matrix, start, end)
    return cost


def part2(fname):
    matrix = expand(read_input(fname))
    start = (0, 0)
    end = (matrix.shape[0] - 1, matrix.shape[1] - 1)
    cost = dijkstra(matrix, start, end)
    return cost


assert 40 == part1("sample.txt")
# assert 527 == part1("input.txt")

assert part2("sample.txt") == 315
logger.info(part2("input.txt"))
