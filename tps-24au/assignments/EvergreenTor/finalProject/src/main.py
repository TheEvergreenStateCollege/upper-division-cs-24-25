from testMaxHeap import MaxHeap

heap = MaxHeap()

player1 = {'name': 'Johnathan Joestar', 'goals_scored': 4}
player2 = {'name': 'Joseph Joestar', 'goals_scored': 3}
player3 = {'name': 'Kujo Jotaro', 'goals_scored': 12}

heap.push(player1)
heap.push(player2)
heap.push(player3)


if __name__ == "__main__":
    print(heap.peek())
    print(heap.size())

    print(str(heap))