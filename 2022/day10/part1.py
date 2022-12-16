import logging

logging.basicConfig(level=logging.INFO)


class State:
    def __init__(self, t=0, X=1):
        self.t = t
        self.X = X
        self.buffer = 0
        self.signal_strength = 0

    def cycle(self, instruction):
        self.t += 1
        # this happens mid-cycle
        if (self.t - 20) % 40 == 0:
            self.signal_strength += self.t * self.X
        # end of cycle
        self.X += self.buffer
        self.buffer = 0
        if instruction.startswith("add"):
            value = int(instruction.split()[-1])
            assert self.buffer == 0
            self.buffer = value
            self.cycle(instruction="noop")


state = State()
with open("sample.txt", "r") as f:
    instructions = f.readlines()
for instruction in instructions:
    state.cycle(instruction)

assert state.signal_strength == 13140, signal_strength


part1 = State()
with open("input.txt", "r") as f:
    instructions = f.readlines()
for instruction in instructions:
    part1.cycle(instruction)

print(part1.signal_strength)
