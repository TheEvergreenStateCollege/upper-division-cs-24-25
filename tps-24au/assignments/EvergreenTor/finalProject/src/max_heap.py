class MaxHeap:
    def __init__(self):
        self.heap = []

    def size(self):
        return len(self.heap)
    
    def push(self,value):
        self.heap.append(value)
        i = len(self.heap) - 1 
        parent = (i - 1) // 2

        while i > 0 and self.heap[i]['goals_scored'] > self.heap[parent]['goals_scored']:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent
            parent = (i - 1) // 2
            

    def peek(self):
        if self.heap == []:
            return None
        else:
            return self.heap[0]
        
    def pop(self):
        
        last_leaf = self.heap.pop()
        old_max = self.heap[0]
        hole = 0
        child = 0

        while hole * 2 <= len(self.heap):
            child = hole * 2
            if child != len(self.heap) and (child + 1) > child:
                child += 1
            if len(self.heap) < 0:
                hole = child
            else:
                break
            
            

    def heapify(self):
        n = len(self.heap)
        # Start from the last non-leaf node and move upward
        for i in range((n // 2) - 1, -1, -1):
            self._sift_down(i)

    def _sift_down(self, i):
        n = len(self.heap)
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Check if left child exists and has more goals_scored than the current node
        if left < n and self.heap[left]['goals_scored'] > self.heap[largest]['goals_scored']:
            largest = left

        # Check if right child exists and has more goals_scored than the current largest node
        if right < n and self.heap[right]['goals_scored'] > self.heap[largest]['goals_scored']:
            largest = right

        # If the largest is not the current node, swap and continue sifting down
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self._sift_down(largest)


        