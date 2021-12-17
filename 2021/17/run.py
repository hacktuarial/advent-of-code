from joblib import Memory

memory = Memory("/tmp")

class Probe:
    def __init__(self, x_velocity, y_velocity, target):
        self.x = 0
        self.y = 0
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.target = target
        self.maximum_y = self.y

    def step(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        if self.x_velocity < 0:
            self.x_velocity += 1
        elif self.x_velocity > 0:
            self.x_velocity -= 1
        else:
            # no change
            pass
        self.y_velocity -= 1  # gravity
        self.maximum_y = max(self.y, self.maximum_y)

    def in_target(self):
        x_min, x_max = self.target[0]
        y_min, y_max = self.target[1]
        return x_min <= self.x <= x_max and y_min <= self.y <= y_max

    def still_has_a_chance(self):
        y_max = self.target[1][1]
        return self.y >= y_max


def reaches_target(velocity):
    target = ((20, 30), (-10, -5))
    probe = Probe(*velocity, target)
    while probe.still_has_a_chance():
        probe.step()
        if probe.in_target():
            return True
    return False


assert reaches_target((7, 2))
assert reaches_target((6, 3))
assert reaches_target((9, 0))
assert not reaches_target((17, -4))



def find_highest_style(target, lim):
    best_x, best_y = (0, 0)
    y_max = -1_000_000
    for x in range(-lim, lim):
        for y in range(-lim, lim):
            probe = Probe(x, y, target)
            while probe.still_has_a_chance():
                probe.step()
            if probe.in_target():
                if probe.maximum_y > y_max:
                    y_max = probe.maximum_y
                    best_x, best_y = x, y
    return ((best_x, best_y), y_max)


@memory.cache
def test_probe(x, y, target):
    probe = Probe(x, y, target)
    while probe.still_has_a_chance():
        probe.step()
    return probe.in_target()


def part2(target, lim):
    n_solutions = 0
    for x in range(-lim, lim):
        for y in range(-lim, lim):
            n_solutions += test_probe(x, y, target)
    return n_solutions



if __name__ == "__main__":
    print(find_highest_style(target=((20, 30), (-10, -5)), lim=20))
    # print(find_highest_style(target=((175, 227), (-134, -79)), lim=200))

    print(part2(target=((175, 227), (-134, -79)), lim=150))
