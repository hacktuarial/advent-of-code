class Counts:
    def __init__(self, *args):
        self.counts = [0] * 9
        for n in args:
            self.counts[n] += 1
        self.steps = 0

    def step(self):
        # 0 -> [6, 8]
        # all others just go i -> i-1
        new_counts = self.counts[1:]
        new_counts.append(self.counts[0])
        new_counts[6] += self.counts[0]
        self.counts = new_counts
        self.steps += 1

    def total(self):
        return sum(self.counts)


if __name__ == "__main__":
    sample_input = [3, 4, 3, 1, 2]
    full_input = "1,2,1,3,2,1,1,5,1,4,1,2,1,4,3,3,5,1,1,3,5,3,4,5,5,4,3,1,1,4,3,1,5,2,5,2,4,1,1,1,1,1,1,1,4,1,4,4,4,1,4,4,1,4,2,1,1,1,1,3,5,4,3,3,5,4,1,3,1,1,2,1,1,1,4,1,2,5,2,3,1,1,1,2,1,5,1,1,1,4,4,4,1,5,1,2,3,2,2,2,1,1,4,3,1,4,4,2,1,1,5,1,1,1,3,1,2,1,1,1,1,4,5,5,2,3,4,2,1,1,1,2,1,1,5,5,3,5,4,3,1,3,1,1,5,1,1,4,2,1,3,1,1,4,3,1,5,1,1,3,4,2,2,1,1,2,1,1,2,1,3,2,3,1,4,5,1,1,4,3,3,1,1,2,2,1,5,2,1,3,4,5,4,5,5,4,3,1,5,1,1,1,4,4,3,2,5,2,1,4,3,5,1,3,5,1,3,3,1,1,1,2,5,3,1,1,3,1,1,1,2,1,5,1,5,1,3,1,1,5,4,3,3,2,2,1,1,3,4,1,1,1,1,4,1,3,1,5,1,1,3,1,1,1,1,2,2,4,4,4,1,2,5,5,2,2,4,1,1,4,2,1,1,5,1,5,3,5,4,5,3,1,1,1,2,3,1,2,1,1"
    c = Counts(*[int(x) for x in full_input.split(",")])
    for _ in range(256):
        c.step()
    print(c.total())    
    if False:
        assert c.counts == [1, 1, 2, 1, 0, 0, 0, 0, 0]
        c.step()
        assert c.counts == [1, 2, 1, 0, 0, 0, 1, 0, 1]
        while c.steps < 18:
            c.step()
        assert c.total() == 26, c.counts
        while c.steps < 80:
            c.step()
        assert c.total() == 5934
