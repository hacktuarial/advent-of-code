class Snailfish:
    def __init__(self, left, right, depth=0):
        self.left = left
        self.right = right
        self.depth = depth

    def reduce(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, Snailfish):
            return False
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"


# print(Snailfish(1, 2))
# print(Snailfish(Snailfish(1, 2), 3))
# print(Snailfish(9, Snailfish(8, 7)))


def read(string: str) -> Snailfish:
    numbers = []
    depth = 0
    for s in string:
        if s == ",":
            continue
        elif s == "[":
            depth += 1
        elif s == "]":
            right = numbers.pop()
            left = numbers.pop()
            numbers.append(Snailfish(left, right, depth))
            depth -= 1
        else:
            numbers.append(int(s))
    return numbers[0]


assert read("[1,2]") == Snailfish(1, 2)

fish = "[[1,9],[8,5]]"
assert str(read(fish)) == fish, str(read(fish))
fish = "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]"
assert str(read(fish)) == fish
read("[[[[1,2],[3,4]],[[5,6],[7,8]]],9]")
