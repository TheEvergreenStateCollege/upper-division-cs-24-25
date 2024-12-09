import heapq

class MaxHeap:
    def __init__(self) -> None:
        self.heap = []
        
    def push(self, player_data):
        heapq.heappush(self.heap, (-player_data['goals_scored'], player_data))

    def peek(self):
        
        if not self.heap:
            return None
        
        _, player_data = self.heap[0]
        return player_data
        
    def size(self):
        return len(self.heap)
        