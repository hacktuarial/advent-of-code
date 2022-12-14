class PuzzleState:
    def __init__(self, head=(0, 0), tail=(0, 0)):
        self.head = head
        self.tail = tail
        self.tail_positions = {self.tail}

    @staticmethod
    def moveOneStep(position, direction):
        if direction == "L":
            new_position = (position[0], position[1] - 1)
        elif direction == "R":
            new_position = (position[0], position[1] + 1)
        elif direction == "U":
            new_position = (position[0] - 1, position[1])
        elif direction == "D":
            new_position = (position[0] + 1, position[1])
        else:
            raise ValueError(f"Unknown direction {direction}")
        return new_position

    def currentPosition(self):
        return [self.head, self.tail]

    def moveTail(self):
        row_diff = abs(self.head[0] - self.tail[0])
        col_diff = abs(self.head[1] - self.tail[1])
        if row_diff <= 1 and col_diff <= 1:
            # this is close enough
            return
        elif row_diff > 0 and col_diff == 0:
            direction = "U" if self.head[0] < self.tail[0] else "D"
            self.tail = self.moveOneStep(self.tail, direction)
            return
        elif row_diff == 0 and col_diff > 0:
            direction = "L" if self.head[1] < self.tail[1] else "R"
            self.tail = self.moveOneStep(self.tail, direction)
            return
        else:
            # diagonal move
            # print(self.currentPosition())
            assert not self.head == self.tail
            # they should not be in the same row or column
            assert not (self.head[0] == self.tail[0] or self.head[1] == self.tail[1]), [
                self.head,
                self.tail,
            ]
            n_steps = 0
            if self.head[0] < self.tail[0]:
                self.tail = self.moveOneStep(self.tail, "U")
                n_steps += 1
            if self.head[0] > self.tail[0]:
                self.tail = self.moveOneStep(self.tail, "D")
                n_steps += 1
            if self.head[1] < self.tail[1]:
                self.tail = self.moveOneStep(self.tail, "L")
                n_steps += 1
            if self.head[1] > self.tail[1]:
                self.tail = self.moveOneStep(self.tail, "R")
                n_steps += 1
            assert n_steps == 2

    def move(self, direction, steps):
        for _ in range(steps):
            self.head = self.moveOneStep(self.head, direction)
            self.moveTail()
            self.tail_positions.add(self.tail)


def run_unit_tests():
    solver = PuzzleState(head=(-1, 4), tail=(0, 3))


def solve(fname):
    with open(fname, "r") as f:
        moves = f.readlines()

    solver = PuzzleState()
    for move in moves:
        move = move.strip().split()
        move[-1] = int(move[-1])
        solver.move(*move)
    return solver


if __name__ == "__main__":
    run_unit_tests()
    actual = solve("sample.txt")
    assert len(actual.tail_positions) == 13, sorted(
        actual.tail_positions, key=lambda p: p
    )

    actual = solve("input.txt")
    print(len(actual.tail_positions))
