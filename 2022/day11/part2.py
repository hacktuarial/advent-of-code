class Monkey:
    def __init__(self, items, operation, divisible, throw_to, gcm):
        self.items = items
        self.operation = operation
        self.divisible: int = divisible
        self.throw_to = throw_to
        self.inspections = 0
        self.gcm = gcm

    def inspect(self):
        self.inspections += 1
        item = self.items.pop(0)
        item = self.operation(item)
        item = item % self.gcm
        return self.throw(item)

    def throw(self, item):
        if (item % self.divisible) == 0:
            return (item, self.throw_to[0])
        else:
            return (item, self.throw_to[1])


def make_operation(operation: str):
    return lambda old: eval(operation)


assert make_operation("old * old")(4) == 16
assert make_operation("old * 2")(4) == 8
assert make_operation("old + 3")(4) == 7


def monkey_factory(lines, gcm):
    assert "Starting items" in lines[0]
    items = lines[0].split(":")[-1].split(", ")
    items = [int(i) for i in items]
    operation = lines[1]
    assert "Operation" in operation
    try:
        operation = make_operation(operation.split("=")[-1])
    except ValueError as e:
        print(operation)
        raise e
    divisible = int(lines[2].split()[-1])
    targets = (int(lines[3].split()[-1]), int(lines[4].split()[-1]))
    return Monkey(items, operation, divisible, targets, gcm)


def run(fname, n_rounds, gcm):
    monkeys = []
    with open(fname, "r") as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        assert lines[i].startswith("Monkey")
        monkey = monkey_factory(lines[i + 1 : i + 6], gcm)
        print("created a monkey")
        monkeys.append(monkey)
        i += 7
    for _ in range(n_rounds):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                item, throw_to = monkey.inspect()
                monkeys[throw_to].items.append(item)
    inspections = [m.inspections for m in monkeys]
    inspections.sort()
    monkey_business = inspections[-1] * inspections[-2]
    return monkey_business


if __name__ == "__main__":
    assert 2713310158 == run("sample.txt", 10_000, gcm=19 * 23 * 13 * 17)
    print(run("input.txt", 10_000, gcm=19 * 3 * 11 * 17 * 5 * 2 * 13 * 7))
