from typing import List, Tuple
from functools import partial, lru_cache
from itertools import permutations
from enum import Enum

import numpy as np


@lru_cache(maxsize=100)
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


DIGITS = [
    set("abcefg"),  # 0
    set("cf"),  # 1
    set("acdeg"),  # 2
    set("acdfg"),  # 3
    set("bcdf"),  # 4
    set("abdfg"),  # 5
    set("abdefg"),  # 6
    set("acf"),  # 7
    set("abcdefg"),  # 8
    set("abcdfg"),  # 9
]


class Translation:
    all_letters = "abcdefg"

    def __init__(self, letters):
        # encrypted -> decrypted
        self.translation: dict = dict(zip(letters, self.all_letters))
        self.letters = tuple(letters)

    def translate(self, string):
        return set(self.translation[s] for s in string)

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
    try:
        encrypted = entry[lengths.index(len(decrypted))]
    except ValueError:
        return True
    return decrypted == set((translation[e] for e in encrypted))


check_one = lambda x, y: check(x, y, set("cf"))
check_four = lambda x, y: check(x, y, set("bcdf"))
check_seven = lambda x, y: check(x, y, set("acf"))
check_eight = lambda x, y: check(x, y, set("abcdefg"))


def is_possible(entry: List[str], translation: Translation):
    all_valid = all(translation.translate(ent) in DIGITS for ent in entry)
    return (
        all_valid
        and check_one(entry, translation)
        and check_four(entry, translation)
        and check_seven(entry, translation)
        and check_eight(entry, translation)
    )


def brute_force(line):
    n_attempts = 0
    for perm in np.random.permutation(list(permutations(Translation.all_letters))):
        t = Translation(perm)
        n_attempts += 1
        if is_possible(line, t):
            return t
    assert n_attempts == factorial(7)
    raise ValueError(f"No solution found for {line}")


one_line = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split()
solution = Translation("deafgbc")
assert solution.translate("ab") == set("cf"), solution.translate("ab")
assert is_possible(one_line, solution)
bad_solution = Translation("aedfgcb")
assert not is_possible(one_line, bad_solution)


# another example for part2
line2 = "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb".split()
assert brute_force(line2).translate("fdgacbe") == DIGITS[8]
assert brute_force(line2).translate("cefdb") == DIGITS[3]
assert brute_force(line2).translate("cefbgd") == DIGITS[9]
assert brute_force(line2).translate("gcbe") == DIGITS[4]

line3 = "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec".split()
assert brute_force(line3).translate("fcgedb") == DIGITS[9]


def part1(lines):
    special_lengths = {2, 3, 4, 7}
    count = 0
    for line in lines:
        output = line.split("|")[1].split()
        for word in output:
            if len(word) in special_lengths:
                count += 1
    # assert count == 26
    # print(count)


assert brute_force(one_line) == solution, brute_force(one_line)

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        part1(lines)
        part2 = 0
        print(len(lines))
        for line in lines:
            left, right = line.split("|")
            left = left.strip()
            solution = brute_force(left.split())
            for i, secret in enumerate(right.split()):
                decoded = solution.translate(secret)
                part2 += DIGITS.index(decoded) * (10 ** (3 - i))
        assert part2 == 61_229, part2
