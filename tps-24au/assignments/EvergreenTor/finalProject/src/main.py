from max_heap import MaxHeap
from dataloader import DataLoader

heap = MaxHeap()

# loader = DataLoader('../data/2015.csv')
# loader = DataLoader('../data/2016.csv')
# loader = DataLoader('../data/2017.csv')
# loader = DataLoader('../data/2018.csv')
# loader = DataLoader('../data/2019.csv')
# loader = DataLoader('../data/2020.csv')
# loader = DataLoader('../data/2021.csv')
# loader = DataLoader('../data/2022.csv')
# loader = DataLoader('../data/2023.csv')
loader = DataLoader('../data/2024.csv')
player_data = loader.load_data()

for player in player_data[:7]:
    heap.push(player)
    print(player)

print("Top player:", heap.peek())

for player in player_data[:7]:
    print(player)
