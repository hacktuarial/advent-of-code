import sys
from dataclasses import dataclass


@dataclass
class Move:
    how_many: int
    from_stack: int
    to_stack: int


class Stack:
    def __init__(self):
        self.items = []
        self.N = 0

    def push(self, x):
        self.items.append(x)
        self.N += 1

    def pop(self):
        x = self.items.pop(self.N - 1)
        self.N = self.N - 1
        return x


def parse_move(move: str):
    words = move.split()
    return Move(
        how_many=int(words[1]),
        from_stack=int(words[-3]) - 1,
        to_stack=int(words[-1]) - 1,
    )


def run(fname):
    is_sample = fname == "sample.txt"
    with open(fname, "r") as f:
        lines = f.readlines()
    sep = lines.index("\n")
    # figure out how many stacks there are
    n_stacks = max((int(c) for c in lines[sep - 1].split()))
    if is_sample:
        assert n_stacks == 3
    stacks = [Stack() for _ in range(n_stacks)]
    # read the lines backwards
    for line in lines[: sep - 1][::-1]:
        for i, stack in enumerate(stacks):
            # positions 1, 5, 9, ...
            element = line[1 + 4 * i]
            if element != " ":
                stack.push(element)
    moves = [parse_move(mv) for mv in lines[sep + 1 :]]
    for move in moves:
        if move.how_many == 1:
            moving = stacks[move.from_stack].pop()
            stacks[move.to_stack].push(moving)
        else:
            moving = [stacks[move.from_stack].pop() for _ in range(move.how_many)]
            moving = moving[::-1]
            for crate in moving:
                stacks[move.to_stack].push(crate)
    return "".join([stack.pop() for stack in stacks])


assert "MCD" == run("sample.txt")

if __name__ == "__main__":
    print(run(sys.argv[1]))
