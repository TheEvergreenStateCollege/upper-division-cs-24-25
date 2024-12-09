import pdb
import sys

coins = [25, 10, 5, 1]

def makeChange(total):
    #pdb.set_trace()
    change = []
    remaining = total
    while remaining > 0:
        for d in coins:
            if d <= remaining:
                change.append(d)
                remaining -= d
                break
    return change

val = 0
if len(sys.argv) > 1:
    val = int(sys.argv[1])
else:
    print("Enter value:")
    val = int(input())

print(makeChange(val))
