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
    n_boards = len(boards)
    has_won = [False] * len(boards)
    for number in numbers:
        for b in range(n_boards):
            board = boards[b]
            boards[b].mark(number)
            if board.has_won():
                # is it the last one?
                is_last = all([has_won[c] for c in range(n_boards) if c != b])
                if is_last:
                    print("This board won last")
                    print(number * board.tally())
                    if "sample" in fname:
                        assert number * board.tally() == 1924
                    sys.exit(0)
                else:
                    has_won[b] = True


if __name__ == "__main__":
    load(sys.argv[1])
