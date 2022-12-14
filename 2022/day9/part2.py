class PuzzleState:
    def __init__(self):
        self.heads = [(0, 0) for _ in range(10)]
        self.tail_positions = {(0, 0)}

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

    def followHead(self, i):
        head = self.heads[i - 1]
        tail = self.heads[i]

        row_diff = abs(head[0] - tail[0])
        col_diff = abs(head[1] - tail[1])
        if row_diff <= 1 and col_diff <= 1:
            # this is close enough
            return
        elif row_diff > 0 and col_diff == 0:
            direction = "U" if head[0] < tail[0] else "D"
            tail = self.moveOneStep(tail, direction)
        elif row_diff == 0 and col_diff > 0:
            direction = "L" if head[1] < tail[1] else "R"
            tail = self.moveOneStep(tail, direction)
        else:
            # diagonal move
            assert not head == tail
            # they should not be in the same row or column
            assert not (head[0] == tail[0] or head[1] == tail[1]), [
                head,
                tail,
            ]
            n_steps = 0
            if head[0] < tail[0]:
                tail = self.moveOneStep(tail, "U")
                n_steps += 1
            if head[0] > tail[0]:
                tail = self.moveOneStep(tail, "D")
                n_steps += 1
            if head[1] < tail[1]:
                tail = self.moveOneStep(tail, "L")
                n_steps += 1
            if head[1] > tail[1]:
                tail = self.moveOneStep(tail, "R")
                n_steps += 1
            assert n_steps == 2
        self.heads[i] = tail

    def move(self, direction, steps):
        for _ in range(steps):
            for i in range(10):
                if i == 0:
                    self.heads[i] = self.moveOneStep(self.heads[i], direction)
                else:
                    self.followHead(i)
            self.tail_positions.add(self.heads[-1])


def solve(fname):
    solver = PuzzleState()
    with open(fname, "r") as f:
        moves = f.readlines()

    for move in moves:
        move = move.strip().split()
        move[-1] = int(move[-1])
        solver.move(*move)
    return solver


if __name__ == "__main__":
    actual = solve("sample2.txt")
    assert len(actual.tail_positions) == 36, sorted(
        actual.tail_positions, key=lambda p: p
    )

    actual = solve("input.txt")
    print(len(actual.tail_positions))
