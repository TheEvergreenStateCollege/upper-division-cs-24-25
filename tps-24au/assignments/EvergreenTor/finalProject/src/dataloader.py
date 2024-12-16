import csv

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        data = []
        try:
            # Open the CSV file
            with open(self.file_path, mode='r') as file:
                # Use DictRead to read the CSV as a list of dictionaries
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        #Extract and validate fields
                        # player_id,player_name,goals_scored,team_name,nationality,age,position,matches_played
                        player_id = row['player_id']
                        player_name = row['player_name']
                        goals_scored = int(row['goals_scored'])
                        team_name = row['team_name']
                        nationality = row['nationality']
                        age = int(row['age'])
                        position = row['position']
                        matches_played = int(row['matches_played'])

                        # Append the clean data
                        data.append({
                            'player_id': player_id,
                            'player_name': player_name,
                            'goals_scored': goals_scored,
                            'team_name': team_name,
                            'nationality': nationality,
                            'age': age,
                            'position': position,
                            'matches_played': matches_played
                        })
                    except (ValueError, KeyError):
                        # Skip rows with missing or invalid data
                        continue
        except FileNotFoundError:
            print(f"Error: The file at {self.file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        return data
    