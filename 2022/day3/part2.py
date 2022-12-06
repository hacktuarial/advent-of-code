import sys
from functools import reduce
from string import ascii_lowercase, ascii_uppercase


def get_priority(letter):
    priorities = ascii_lowercase + ascii_uppercase
    return 1 + priorities.index(letter)





def score(fname):
    with open(fname, "r") as f:
        rucksacks = f.readlines()
    rucksacks = [sack.strip() for sack in rucksacks]
    total_priority = 0
    for i in range(0, len(rucksacks), 3):
        overlap = reduce(lambda x, y: set(x).intersection(y), rucksacks[i:i+3])
        assert len(overlap) == 1, (rucksacks[i:i+3], overlap)
        total_priority += get_priority(overlap.pop())
    return total_priority


assert score("sample.txt") == 70

if __name__ == "__main__":
    fname = sys.argv[1]
    print(score(fname))
