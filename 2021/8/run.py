from typing import List, Tuple
from functools import partial
from itertools import permutations


class Translation:
    letters = "abcdefg"
    def __init__(self, letters):
        # encrypted -> decrypted
        self.translation: dict = dict(zip(letters, self.letters))
        self.letters = tuple(letters)

    def __hash__(self):
        return hash(self.letters)

    def __getitem__(self, key):
        # behaves like a dictionary
        return self.translation[key]

    def __eq__(self, other):
        return self.letters == other.letters

    def __str__(self):
        return "".join(self.letters)

def check(entry, translation, decrypted):
    lengths = [len(seg) for seg in entry]
    encrypted = entry[lengths.index(len(decrypted))]
    return decrypted == set((translation[e] for e in encrypted))

check_one = lambda x, y: check(x, y, set("cf"))
check_four = lambda x, y: check(x, y, set("bcdf"))
check_seven = lambda x, y: check(x, y, set("acf"))
check_eight = lambda x, y: check(x, y, set("abcdefg"))


def is_possible(entry: List[str], translation: Translation):
    return check_one(entry, translation) and check_four(entry, translation) and \
check_seven(entry, translation) and check_eight(entry, translation)

def part2(line):
    # breadth first search of possible solutions
    queue = []
    visited = dict()
    # find a starting point
    for root in permutations(Translation.letters):
        solution = Translation(root)
        if is_possible(line, solution):
            break
    visited[solution] = True
    queue.append(solution)
    while len(queue) > 0:
        v = queue.pop(0)


def brute_force(line):
    for perm in permutations(Translation.letters):
        t = Translation(perm)
        if is_possible(line, t):
            return t

one_line = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split()
solution = Translation("deafgbc")
assert is_possible(one_line, solution)
bad_solution = Translation("aedfgcb")
assert not is_possible(one_line, bad_solution)




def part1(lines):
    special_lengths = {2, 3, 4, 7}
    count = 0
    for line in lines:
        output = line.split("|")[1].split()
        for word in output:
            if len(word) in special_lengths:
                count += 1
    # assert count == 26
    print(count)


with open("input.txt", "r") as f:
    lines = f.readlines()
    part1(lines)

assert brute_force(one_line) == solution, brute_force(one_line)
