from typing import List
from collections import Counter

import fire


def most_common(lines, i) -> str:
    chars = [line[i] for line in lines]
    c = Counter(chars).most_common(1)
    return c[0][0]

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

def run(fname):
    with open(fname, "rb") as f:
        lines = f.readlines()
    lines = [s.decode("utf-8").strip() for s in lines]
    gamma = get_gamma(lines)
    eps = get_epsilon(gamma)
    print("gamma=%s, epsilon=%s in binary" % (gamma, eps))
    eps = binary_to_int(eps)
    gamma = binary_to_int(gamma)
    print("gamma=%d, epsilon=%d, product=%d" % (gamma, eps, gamma*eps))

if __name__ == "__main__":
    fire.Fire(run)



