import numpy as np


class Board:
    def __init__(self, numbers: np.array):
        self.numbers = numbers
        self.marked = np.zeros_like(numbers).astype(bool)
        self.dim = numbers.shape[0]
        assert numbers.shape[1] == numbers.shape[0], numbers
        assert len(numbers.shape) == 2

    def mark(self, number):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.numbers[i, j] == number:
                    self.marked[i, j] = True

    def has_won(self):
        for i in range(self.dim):
            # row
            if sum(self.marked[i, :]) == self.dim:
                return True
            # column
            if sum(self.marked[:, i]) == self.dim:
                return True
        return False

    def tally(self):
        return self.numbers[~self.marked].sum()

    def __str__(self):
        return str(self.numbers)
