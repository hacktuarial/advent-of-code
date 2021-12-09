
with open("input.txt", "r") as f:
    lines = f.readlines()
special_lengths = {2, 3, 4, 7}
count = 0
for line in lines:
    output = line.split("|")[1].split()
    for word in output:
        if len(word) in special_lengths:
            count += 1
# assert count == 26
print(count)
