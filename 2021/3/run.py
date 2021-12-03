from typing import List
from collections import Counter

import fire

ONE = "1"
ZERO = "0"



def most_common(lines, i: int) -> str:
    chars = [line[i] for line in lines]
    c = Counter(chars)
    # assert set(c.keys()) == {"0", "1"}, c.keys()
    if c[ZERO] > c[ONE]:
        return ZERO
    else:
        # in case of tie, return 1
        return ONE

def get_gamma(lines) -> str:
    n = len(lines[0])
    output: List[str] = ["-"] * n
    for i in range(n):
        output[i] = most_common(lines, i)
    return "".join(output)

def binary_to_int(binary: str) -> int:
    n = len(binary)
    return sum([int(b) * 2**(n-i-1) for i, b in enumerate(binary)])


assert binary_to_int('10110') == 22, binary_to_int('10110')
assert binary_to_int('01001') == 9

def get_epsilon(gamma: str) -> str:
    bits = [1 - int(g) for g in gamma]
    return "".join([str(b) for b in bits])


def get_oxygen(lines) -> str:
    oxygen = ""
    n = len(lines[0])
    filtered_lines = lines[:]
    for i in range(n):
        bit = most_common(filtered_lines, i)
        oxygen += bit
        filtered_lines = [line for line in filtered_lines if line[i] == bit]
    return oxygen

def run(fname, part=2):
    with open(fname, "rb") as f:
        all_lines = f.readlines()
    all_lines = [s.decode("utf-8").strip() for s in all_lines]
    if part == 1:
        gamma = get_gamma(all_lines)
        eps = get_epsilon(gamma)
        print("gamma=%s, epsilon=%s in binary" % (gamma, eps))
        eps = binary_to_int(eps)
        gamma = binary_to_int(gamma)
        answer = eps * gamma
        print("gamma=%d, epsilon=%d, product=%d" % (gamma, eps, answer))
        if fname == "sample_input.txt":
            assert answer == 198
        else:
            assert answer == 3912944
    else:
        oxygen = get_oxygen(all_lines)
        assert binary_to_int(oxygen) == 23, oxygen


if __name__ == "__main__":
    fire.Fire(run)



