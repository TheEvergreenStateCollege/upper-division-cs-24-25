from dataloader import DataLoader
from max_heap import MaxHeap

class Leaderboard:
    def __init__(self, csv_file):
        # Reference to the CSV file path
        self.data_source = csv_file
        # Initialize the MaxHeap
        self.max_heap = MaxHeap()
        # Create an instance of DataLoader and load the data
        loader = DataLoader(self.data_source)
        self.players_data = loader.load_data()

        for player in self.players_data:
            self.max_heap.push(player)

    def __str__(self):
        result = "Leaderboard:\n"
        result += f"{'Name':<20}{'Goals':<10}{'Team':<20}{'Nationality':<15}{'Age':<5}{'Position':<10}{'Matches Played':<15}\n"
        result += "-" * 95 + "\n"

        temp_heap = MaxHeap()
        temp_heap.heap = self.max_heap.heap[:]

        while temp_heap.size() > 0:
            player = temp_heap.peek()
            result += f"{player['player_name']:<20}{player['goals_scored']:<10}{player['team_name']:<20}{player['nationality']:<15}{player['age']:<5}{player['position']:<10}{player['matches_played']:<15}\n"
            temp_heap.heap[0], temp_heap.heap[-1] = temp_heap.heap[-1], temp_heap.heap[0]
            temp_heap.heap.pop()
            temp_heap._sift_down(0)

        return result
