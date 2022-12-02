from rochambeau import *

lookup = {
    "A": Rock(),
    "B": Paper(),
    "C": Scissors(),
    # only for part 1
    # "X": Rock(),
    # "Y": Paper(),
    # "Z": Scissors(),
}


def score(opponent, me) -> int:
    if opponent < me:
        return 6 + me.score
    elif opponent == me:
        return 3 + me.score
    else:
        return 0 + me.score


if __name__ == "__main__":
    options = [Rock(), Paper(), Scissors()]
    total_score = 0
    with open("input.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        left, right = line.split()
        left = lookup[left]
        if right == "X":
            # lose
            i = 0
            right = options[i]
            while right >= left:
                i += 1
                right = options[i]
        elif right == "Y":
            # draw
            right = left
        else:
            # win
            i = 0
            right = options[i]
            while right <= left:
                i += 1
                right = options[i]

        total_score += score(left, right)
    print(total_score)
