import sys

import numpy as np


class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_string(cls, xy: str):
        split = xy.split(",")
        return Pair(int(split[0]), int(split[1]))


def is_horizontal(pair1: Pair, pair2: Pair):
    return pair1.x == pair2.x


def is_vertical(pair1: Pair, pair2: Pair):
    return pair1.y == pair2.y


def get_segment(line: str):
    arrow = "->"
    pair0, pair1 = line.split(arrow)
    pair0 = Pair.from_string(pair0)
    pair1 = Pair.from_string(pair1)
    return pair0, pair1


def read(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    segments = [get_segment(line) for line in lines]
    dim: int = 1 + max(max(a.x, a.y, b.x, b.y) for a, b in segments)
    counts = np.zeros((dim, dim))
    for seg in segments:
        if is_horizontal(*seg):
            ymin = min(seg[0].y, seg[1].y)
            ymax = max(seg[0].y, seg[1].y)
            x = seg[0].x
            for y in range(ymin, ymax + 1):
                counts[x, y] += 1
        elif is_vertical(*seg):
            xmin = min(seg[0].x, seg[1].x)
            xmax = max(seg[0].x, seg[1].x)
            y = seg[0].y
            for x in range(xmin, xmax + 1):
                counts[x, y] += 1
        else:
            # diagonal
            length = abs(seg[0].x - seg[1].x) + 1
            x_decreasing = seg[0].x > seg[1].x
            y_decreasing = seg[0].y > seg[1].y
            for i in range(length):
                xstep = -i if x_decreasing else i
                ystep = -i if y_decreasing else i
                counts[seg[0].x + xstep, seg[0].y + ystep] += 1
    print(counts.T)
    total = (counts > 1).sum()
    if "sample" in fname:
        assert total == 12, total
    print(total)


if __name__ == "__main__":
    read(sys.argv[1])
