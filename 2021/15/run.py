import sys
from typing import List, Tuple

from logzero import logger
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
    min_value = np.inf
    which_min = None
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if (i, j) in known:
                continue
            if matrix[i, j] < min_value:
                which_min = (i, j)
                min_value = matrix[i, j]
    return which_min


def dijkstra(matrix, start: Tuple, end: Tuple):
    known = {start}
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
        known = known.union({v})
    return distances[end[0], end[1]]


def part1(fname):
    matrix = read_input(fname)
    logger.info(matrix.shape)
    # assuming it's square
    start = (0, 0)
    end = (matrix.shape[0] - 1, matrix.shape[1] - 1)
    cost = dijkstra(matrix, start, end)
    return cost


assert 40 == part1("sample.txt")
