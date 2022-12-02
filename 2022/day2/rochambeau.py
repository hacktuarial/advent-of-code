from functools import total_ordering


@total_ordering
class Paper:
    score = 2

    def __eq__(self, other):
        return isinstance(other, Paper)

    def __lt__(self, other):
        return isinstance(other, Scissors)

    def __gt__(self, other):
        return isinstance(other, Rock)


@total_ordering
class Scissors:
    score = 3

    def __eq__(self, other):
        return isinstance(other, Scissors)

    def __lt__(self, other):
        return isinstance(other, Rock)

    def __gt__(self, other):
        return isinstance(other, Paper)


@total_ordering
class Rock:
    score = 1

    def __eq__(self, other):
        return isinstance(other, Rock)

    def __lt__(self, other):
        return isinstance(other, Paper)

    def __gt__(self, other):
        return isinstance(other, Scissors)
