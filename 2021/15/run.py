import sys
from typing import List, Tuple

def read_input(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    matrix = []
    for line in lines:
        line = line.strip()
        row = []
        for x in line:
            row.append(int(x))
        matrix.append(row )
    return matrix


def get_neighbors(matrix, row, col):
    up = matrix[row-1, col]
    down = matrix[row+1, col]
    left = matrix[row, col-1]
    right = matrix[row, col+1]
    return [up, down, left, right]

def find_min_distance(matrix):
    min = (0, 0)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] < matrix[min[0]][min[1]]:
                min = (i, j)
    return min

def dijkstra(matrix, start: Tuple, end: Tuple):
    known = {start}
    distances = [[sys.maxint] for row in matrix for x in  row]
    for neighbor in get_neighbors(matrix, *start):
        # no cost incurred at starting vertex
        distances[neighbor[0]][neighbor[1]] = distances[neighbor[0]][neighbor[1]]
    last = start
    while last != end:
        v = find_min_distance(distances)
        for neighbor in get_neighbors(matrix, *v):
            current_distance = distances[neighbor[0]][neighbor[1]]
            new_distance = distances[v[0]][v[1]] + matrix[neighbor[0]][neighbor[1]]
            distances[neighbor[0]][neighbor[1]] = min(current_distance, new_distance)
            last = v
            known = known.update(v)
    return distances[end[0], end[1]]


def part1(fname):
    matrix = read_input(fname)
    # assuming it's square
    cost = dijkstra(matrix, (0, 0), (len(matrix), len(matrix)))
    return cost

part1("sample.txt")