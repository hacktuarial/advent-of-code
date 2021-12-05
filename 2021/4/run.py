import sys

import numpy as np

from board import Board

DIM = 5

def load_boards(lines):
    boards = []
    rows = []
    i = 0
    while i < len(lines):
        if lines[i] == "\n":
            rows = []
            i += 1
        while len(rows) < DIM:
            row = [int(n) for n in lines[i].strip().split()]
            rows.append(row)
            i += 1
        board = Board(np.array(rows))
        boards.append(board)
    return boards


def load(fname):
    with open(fname, "r") as f:
        all_lines = f.readlines()
    numbers = all_lines.pop(0).split(",")
    numbers = [int(n) for n in numbers]
    boards = load_boards(all_lines)
    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.has_won():
                print("This board won!")
                if "sample" in fname:
                    assert number*board.tally() == 4512
                sys.exit(0)


if __name__ == "__main__":
    load("sample_input.txt")