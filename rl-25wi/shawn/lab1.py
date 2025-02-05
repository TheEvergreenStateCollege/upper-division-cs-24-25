import random

def randn(n):
    return [random.randint(1,100) for _ in range(n)]

def avg(nums):
    return sum(nums) / len(nums)

print(avg(randn(20)))

def avgn(n):
    total = 0
    for _ in range(n):
        total += random.randint(1,100)
    return total / n

print(avgn(20))
