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


def get_neighbors(matrix, row, col):
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


assert set(get_neighbors(np.ones((2, 2)), 0, 0)) == set([(0, 1), (1, 0)])


def find_min_distance(matrix):
    """Returns the index of the minimum value"""
    min = (0, 0)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] < matrix[min[0], min[1]]:
                min = (i, j)
    return min


def dijkstra(matrix, start: Tuple, end: Tuple):
    known = {start}
    distances = np.ones(matrix.shape) * np.inf
    for neighbor in get_neighbors(matrix, *start):
        logger.info(neighbor)
        # no cost incurred at starting vertex
        distances[neighbor[0], neighbor[1]] = distances[neighbor[0], neighbor[1]]
    last = start
    while last != end:
        v = find_min_distance(distances)
        for neighbor in get_neighbors(matrix, *v):
            current_distance = distances[neighbor[0], neighbor[1]]
            new_distance = distances[v[0], v[1]] + matrix[neighbor[0], neighbor[1]]
            distances[neighbor[0], neighbor[1]] = min(current_distance, new_distance)
        last = v
        known.update(v)
        logger.info("I've visited %d vertices", len(known))
    return distances[end[0], end[1]]


def part1(fname):
    matrix = read_input(fname)
    logger.info(matrix.shape)
    # assuming it's square
    cost = dijkstra(matrix, (0, 0), (len(matrix), len(matrix)))
    return cost


part1("sample.txt")
