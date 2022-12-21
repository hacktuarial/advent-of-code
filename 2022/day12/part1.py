"""
TODO use breadth first search
instead of
depth first search
BFS is guaranteed to find the shortest path
"""

import pdb
from typing import List, Tuple
from string import ascii_lowercase
import numpy as np

def find_char(X, ch):
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if X[i, j] ==ch:
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


class DepthFirstSearch:
    def __init__(self, X, start):
        self.X = X
        self.visited = np.ones_like(X, dtype=float) * np.inf
        self.start = start

    def run(self):
        self.visit(self.start, 0)
        loc = find_char(self.X, "E")
        return self.visited[loc]

    def visit(self, point, path_length) -> int:
        if path_length < self.visited[point]:
            self.visited[point] = path_length
        for neighbor in get_neighbors(self.X, *point):
            if path_length + 1 <= self.visited[neighbor]:
                self.visit(neighbor, path_length + 1)


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

def solve(fname):
    mat = read(fname)
    solver = DepthFirstSearch(X=mat, start=find_char(mat, "S"))
    return solver.run()


if __name__ == "__main__":
    sample = solve("sample.txt")
    assert sample == 31

    part1 = solve("input.txt")
    print(part1)
