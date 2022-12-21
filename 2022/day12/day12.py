"""
Breadth First Search is guaranteed to find the shortest path
"""

import pdb
from typing import List, Tuple
from string import ascii_lowercase
import numpy as np


def find_char(X, ch):
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if X[i, j] == ch:
                return (i, j)
    raise ValueError


def get_neighbors(X, i, j) -> List[Tuple[int, int]]:
    nrow, ncol = X.shape
    current = X[i, j]
    if current == "S":
        current = "a"
    elif current == "E":
        current = "z"
    potential_neighbors = []
    if i > 0:
        # up
        potential_neighbors.append((i - 1, j))
    if i < len(X) - 1:
        # down
        potential_neighbors.append((i + 1, j))
    if j > 0:
        # left
        potential_neighbors.append((i, j - 1))
    if j < ncol - 1:
        # right
        potential_neighbors.append((i, j + 1))
    current_index = ascii_lowercase.index(current)
    delta = [0] * len(potential_neighbors)
    for i, (row, col) in enumerate(potential_neighbors):
        height = X[row, col]
        if height == "E":
            height = "z"
        elif height == "S":
            height = "a"
        delta[i] = ascii_lowercase.index(height) - current_index
    res = [n for (d, n) in zip(delta, potential_neighbors) if d <= 1]
    return res


class BreadthFirstSearch:
    def __init__(self, X, start):
        self.X = X
        self.visited = np.zeros_like(X, dtype=bool)
        self.path_length = np.ones_like(X, dtype=float) * np.inf
        self.path_length[start] = 0
        self.to_visit = [
            start,
        ]

    def run(self):
        while len(self.to_visit) > 0:
            point = self.to_visit.pop(0)
            if self.X[point] == "E":
                return self.path_length[point]
            for neighbor in get_neighbors(self.X, *point):
                if not self.visited[neighbor]:
                    self.visited[neighbor] = True
                    self.path_length[neighbor] = self.path_length[point] + 1
                    self.to_visit.append(neighbor)
        return np.inf


def read(fname):
    with open(fname, "r") as f:
        mat = f.readlines()
    mat = [m.replace("\n", "") for m in mat]
    nrow = len(mat)
    ncol = len(mat[0])
    X = np.empty(shape=(len(mat), len(mat[0])), dtype=str)
    for i in range(nrow):
        for j in range(ncol):
            X[i, j] = mat[i][j]
    return X


def solve(fname, start=None):
    mat = read(fname)
    start = start or find_char(mat, "S")
    solver = BreadthFirstSearch(X=mat, start=start)
    return solver.run()


if __name__ == "__main__":
    sample = solve("sample.txt")
    assert sample == 31, sample

    part1 = solve("input.txt")
    print(part1)

    # part 2
    best_solution = np.inf
    mat = read("input.txt")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] == "a":
                this_solution = BreadthFirstSearch(X=mat, start=(i, j)).run()
                best_solution = min(best_solution, this_solution)
    print(best_solution)
