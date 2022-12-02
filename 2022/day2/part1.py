from enum import Enum


class Paper:
    score = 2
    def __eq__(self, other):
        return isinstance(other, Paper)
    def __lt__(self, other):
        return isinstance(other, Scissors)
    def __gt__(self,other):
        return isinstance(other, Rock)

class Scissors:
    score = 3
    def __eq__(self, other):
        return isinstance(other, Scissors)
    def __lt__(self, other):
        return isinstance(other, Rock)
    def __gt__(self,other):
        return isinstance(other, Paper)

class Rock:
    score = 1
    def __eq__(self, other):
        return isinstance(other, Rock)
    def __lt__(self, other):
        return isinstance(other, Paper)
    def __gt__(self,other):
        return isinstance(other, Scissors)


lookup = {"A": Rock(), "B": Paper(), "C": Scissors(),
        "X": Rock(),
          "Y": Paper(),
          "Z": Scissors()}



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
