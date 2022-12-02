from enum import Enum
from rochambeau import *


lookup = {
    "A": Rock(),
    "B": Paper(),
    "C": Scissors(),
    "X": Rock(),
    "Y": Paper(),
    "Z": Scissors(),
}


def score(opponent, me) -> int:
    if opponent < me:
        return 6 + me.score
    elif opponent == me:
        return 3 + me.score
    else:
        return 0 + me.score


if __name__ == "__main__":
    total_score = 0
    with open("input.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        left, right = line.split()
        total_score += score(lookup[left], lookup[right])
    print(total_score)
