import sys
from string import ascii_lowercase, ascii_uppercase


def get_priority(letter):
    priorities = ascii_lowercase + ascii_uppercase
    return 1 + priorities.index(letter)


assert get_priority("p") == 16
assert get_priority("L") == 38


def find_overlap(contents):
    N = len(contents) // 2
    left = contents[:N]
    right = contents[N:]
    return set(left).intersection(right)


def score(fname):
    with open(fname, "r") as f:
        rucksacks = f.readlines()
    total_priority = 0
    for sack in rucksacks:
        overlap = find_overlap(sack).pop()
        total_priority += get_priority(overlap)
    return total_priority


assert score("sample.txt") == 157

if __name__ == "__main__":
    fname = sys.argv[1]
    print(score(fname))
