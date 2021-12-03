from typing import List
from collections import Counter

import fire

ONE = "1"
ZERO = "0"


def swap_bit(x):
    if x == ONE:
        return ZERO
    elif x == ZERO:
        return ONE
    else:
        raise ValueError(x)


def count_values(lines, i) -> Counter:
    return Counter([line[i] for line in lines])

def most_common(lines, i: int) -> str:
    c = count_values(lines, i)
    if c[ZERO] > c[ONE]: # counter defaults to 0 for unseen values
        return ZERO
    else:
        # in case of tie, return 1
        return ONE

def least_common(lines, i):
    c = count_values(lines, i)
    if c[ONE] < c[ZERO]:  # counter defaults to 0 for unseen values
        return ONE
    else:
        # default to 0
        return ZERO


assert most_common([], 0) == ONE
assert least_common([], 0) == ZERO



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

def get_co2_scrubbing(lines):
    answer = ""
    n = len(lines[0])
    filtered_lines = lines[:]
    for i in range(n):
        bit = least_common(filtered_lines, i)
        answer += bit
        filtered_lines = [line for line in filtered_lines if line[i] == bit]
        if len(filtered_lines) == 1:
            line = filtered_lines[0]
            return answer + line[i+1:]




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
        co2_scrubbing = get_co2_scrubbing(all_lines)
        if "sample" in fname:
            assert binary_to_int(oxygen) == 23, oxygen
            assert binary_to_int(co2_scrubbing) == 10, co2_scrubbing
        else:
            oxygen = binary_to_int(oxygen)
            co2 = binary_to_int(co2_scrubbing)
            print(oxygen * co2)


if __name__ == "__main__":
    fire.Fire(run)



