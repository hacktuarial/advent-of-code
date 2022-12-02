max_so_far = 0
running_total = 0
with open("input.txt", "r") as f:
    while True:
        line = f.readline()
        if not line:
            # end of file
            break
        if line == "\n":
            max_so_far = max(max_so_far, running_total)
            running_total = 0
        else:
            running_total += int(line)

print("The max was %d" % max_so_far)
