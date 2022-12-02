N = 3
max_so_far = [0] * N
running_total = 0
with open("input.txt", "r") as f:
    while True:
        line = f.readline()
        if not line:
            # end of file
            break
        if line == "\n":
            if running_total > min(max_so_far):
                max_so_far[0] = running_total
                # keep it sorted
                max_so_far = sorted(max_so_far)
            running_total = 0
        else:
            running_total += int(line)

print("The max was %d" % sum(max_so_far))
