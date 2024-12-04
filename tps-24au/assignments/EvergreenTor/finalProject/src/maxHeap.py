import heapq

class MaxHeap:
    def __init__(self) -> None:
        self.heap = []
        
    def push(self, player_data):
        heapq.heappush(self.heap, (-player_data['goals_scored'], player_data))
        