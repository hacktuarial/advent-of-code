import sys



if __name__ == "__main__":
    fname = sys.argv[1]
    window = int(sys.argv[2])
    with open(fname, "r") as f:
        numbers = [int(n) for n in f.readlines()]

    increases = 0
    for i in range(0, len(numbers)-window):
        previous = sum(numbers[i: i + window])
        current = sum(numbers[i+1:i+1+window])
        if previous < current:
            increases += 1
    print(increases)
