from typing import List, Tuple
from functools import partial


def check(entry, translation, decrypted):
    lengths = [len(seg) for seg in entry]
    encrypted = entry[lengths.index(len(decrypted))]
    return decrypted == set((translation[e] for e in encrypted))

check_one = lambda x, y: check(x, y, set("cf"))
check_four = lambda x, y: check(x, y, set("bcdf"))
check_seven = lambda x, y: check(x, y, set("acf"))
check_eight = lambda x, y: check(x, y, set("abcdefg"))


def check_four(entry, translation):
    lengths = [len(seg) for seg in entry]
    decrypted = set("bcdf")
    encrypted = entry[lengths.index(len(decrypted))]
    return decrypted == set((translation[e] for e in encrypted))

def check_seven(entry, translation):
    lengths = [len(seg) for seg in entry]
    decrypted = set("acf")
    encrypted = entry[lengths.index(len(decrypted))]
    return decrypted == set((translation[e] for e in encrypted))

def check_eight(entry, translation):
    lengths = [len(seg) for seg in entry]
    decrypted = set("abcdefg")
    encrypted = entry[lengths.index(len(decrypted))]
    return decrypted == set((translation[e] for e in encrypted))

def is_possible(entry: List[str], translation: dict):
    assert set(translation.keys()) == set(translation.values())
    assert set(translation.keys()) == set("abcdefg")
    return check_one(entry, translation) and check_four(entry, translation) and \
check_seven(entry, translation) and check_eight(entry, translation)


one_line = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split()
solution = {"d": "a", "e": "b", "a": "c", "f": "d", "g": "e", "b": "f", "c": "g"}
assert is_possible(one_line, solution)
bad_solution = {"d": "b", "e": "a", "a": "c", "f": "d", "g": "e", "b": "f", "c": "g"}
assert not is_possible(one_line, bad_solution)


def part2(lines):


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
