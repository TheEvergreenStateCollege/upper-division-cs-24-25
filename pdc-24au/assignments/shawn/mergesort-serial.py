def merge(first, last):
    out = []
    while first and last:
        if first[0] <= last[0]:
            out.append(first.pop(0))
        else:
            out.append(last.pop(0))
    return out + first + last

def mergesort(lst):
    if len(lst) == 1:
        return lst
    mid = len(lst) // 2
    first = mergesort(lst[:mid])
    last = mergesort(lst[mid:])
    return merge(first, last)

sample = [12, 63, -8, 15, 82, -10]
print (mergesort(sample))
