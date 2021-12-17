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


def reaches_target(velocity, max_steps):
    target = ((20, 30), (-10, -5))
    probe = Probe(*velocity, target)
    for _ in range(max_steps):
        probe.step()
        if probe.in_target():
            return True
    return False


assert reaches_target((7, 2), 100)
assert reaches_target((6, 3), 100)
assert reaches_target((9, 0), 100)
assert not reaches_target((17, -4), 100)

def optimize_me(velocity):
    # sample
    target = ((20, 30), (-10, -5))
    probe = Probe(*velocity, target)
    for _ in range(100):
        probe.step()
        if probe.in_target():
            return -1 * probe.maximum_y
    # never reached target
    return 100_000

from scipy.optimize import minimize

solution = minimize(optimize_me, (10, -3))
print(solution)

