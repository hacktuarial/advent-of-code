import logging

logging.basicConfig(level=logging.INFO)


class State:
    def __init__(self, t=0, X=1):
        self.t = t
        self.X = X
        self.buffer = 0
        self.signal_strength = 0
        self.part2 = ["0"] * 241

    def draw(self):
        t = self.t % 40 - 1
        if self.X - 1 <= t <= self.X + 1:
            self.part2[self.t] = "#"
        else:
            self.part2[self.t] = "."

    def cycle(self, instruction):
        self.t += 1
        # this happens mid-cycle
        if (self.t - 20) % 40 == 0:
            self.signal_strength += self.t * self.X
        self.draw()
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
for i in range(0, 240, 40):
    print("".join(state.part2[i : i + 40]))

part1 = State()
with open("input.txt", "r") as f:
    instructions = f.readlines()
for instruction in instructions:
    part1.cycle(instruction)

print(f"signal strength={part1.signal_strength}")
for i in range(0, 240, 40):
    print("".join(part1.part2[i : i + 40]))
