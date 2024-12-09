import pdb

coins = [25, 10, 5, 4, 1]

def makeChange(c):
    pdb.set_trace()
    change = []
    remaining = c
    while remaining > 0:
        for d in coins:
            if d <= remaining:
                change.append(d)
                remaining -= d
                break
    return change

print(makeChange(49))
