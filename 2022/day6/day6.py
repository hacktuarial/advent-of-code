from functools import partial


def part1(s: str, width=4) -> int:
    for i in range(width - 1, len(s)):
        substring = sorted(s[(i - width) : i])
        if len(set(substring)) == width:
            return i
    return -1


part2 = partial(part1, width=14)


assert part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
assert part1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
assert part1("nppdvjthqldpwncqszvftbrmjlhg") == 6
assert part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
assert part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

assert part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19

with open("input.txt", "r") as f:
    stream = f.read()
print(part1(stream))
print(part2(stream))
