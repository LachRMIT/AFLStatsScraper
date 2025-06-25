class Round:
    
    def __init__(self, round_value, round_name: str, round_year):
        self.round_value = round_value
        self.round_name = round_name
        self.round_year = round_year
        self.games = []
        
    def __str__(self):
        return f"Round {self.round_value} with {len(self.games)} games"
    
    def __len__(self):
        return (len(self.games))
    
    def add_game(self, game):
        self.games.append(game)
    
    def print_games(self):
        for game in self.games:
            print(game)
    
    def get_game(self, game_number):
        return self.games[game_number - 1]
    
    def get_round_number(self):
        return self.round_no