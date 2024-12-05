from mpi4py import MPI

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

lst = [12, 63, -8, 15, 82, -10]

# MPI starts here
comm = MPI.COMM_WORLD
# size = number of processes
size = comm.Get_size()
# rank = process id
rank = comm.Get_rank()

if rank == 0:
    data = []
    # get the size of each chunk
    count = len(lst) // size
    # fill the chunks with data
    stop = 0
    for i in range(size):
        start = i * count
        stop = (i+1) * count
        # append a chunk for each process
        data.append(lst[start:stop])
    # distribute remainder
    while stop < len(lst):
        data[len(lst) % size].append(lst.pop())
else:
    data = None

# scatter the data to the workers
data = comm.scatter(data, root=0)
# sort each chunk
data = mergesort(data)
# collect the results
data = comm.gather(data, root=0)

# merge the sorted chunks
if rank == 0:
    out = data.pop(0)
    while data:
        out = merge(out, data.pop(0))
    print(out)
