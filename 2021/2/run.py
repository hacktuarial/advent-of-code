import fire


class Position:
    def __init__(self):
        self.x = 0
        self.depth = 0
        self.aim = 0

    def forward(self, n):
        self.x += n
        self.depth += self.aim * n
        return self

    def up(self, n):
        self.aim -= n
        return self

    def down(self, n):
        self.aim += n
        return self

    def report(self):
        print(f"I am at depth={self.x}, depth={self.depth}, and aim={self.aim}")
        print("depth * position = %d" % (self.depth * self.x))
        return self


def run(fname):
    position = Position()
    with open(fname, "r") as f:
        lines = f.readlines()
    for line in lines:
        method, n = line.split(" ")
        position = getattr(position, method)(int(n))
    position.report()


if __name__ == "__main__":
    fire.Fire(run)
