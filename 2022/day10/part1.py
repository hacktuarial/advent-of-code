
import logging
logging.basicConfig(level=logging.INFO)

with open("sample.txt", "r") as f:
    instructions = f.readlines()

t = 0
X = 1
signal_strength = 0
for instruction in instructions:
    if instruction.startswith("noop"):
        t += 1
        logging.debug(t, X)
        continue
    operation, value = instruction.split()
    assert operation == "addx"
    value = int(value)
    for i in range(2):
        t += 1
        if (t - 20) % 40 == 0:
            logging.info(f"Signal strength at time {t} is {t*X}")
            signal_strength += t * X
    X += value
    logging.debug(t, X)
            
                    
                

assert signal_strength == 13140, signal_strength
