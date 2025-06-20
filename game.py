class Game:
    def __init__(self, game_id, year, round, home_team, away_team, winning_team, margin):
        self.game_id = game_id
        self.year = year
        self.round = round
        self.home_team = home_team
        self.away_team = away_team
        self.winning_team = winning_team
        self.margin = margin
        
    def __str__(self):
        return (f"Game {self.game_id} of Round {self.round}, {self.year}. "
                f"{self.home_team.get_name()} v {self.away_team.get_name()}. "
                f"{self.winning_team.get_name()} won by {self.margin}")

class Team:
    team_lookup = {
        "The Draw": 0,
        "Adelaide": 1,
        "Brisbane Lions": 2,
        "Carlton": 3,
        "Collingwood": 4,
        "Essendon": 5,
        "Fremantle": 6,
        "Geelong": 7,
        "Gold Coast": 8,
        "Greater Western Sydney": 9,
        "Hawthorn": 10,
        "Melbourne": 11,
        "North Melbourne": 12,
        "Port Adelaide": 13,
        "Richmond": 14,
        "St Kilda": 15,
        "Sydney": 16,
        "West Coast": 17,
        "Western Bulldogs": 18,
    }

    def __init__(self, name):
        self.name = name
        self.team_id = self.team_lookup.get(name)
        if self.team_id is None:
            raise ValueError(f"Unknown team name: {name}")
        
    def __str__(self):
        return f"Team Name: {self.name}, Team ID: {self.team_id}"
    
    def get_name(self):
        return self.name
    
class Round:
    def __init__(self, round_number):
        self.round_no = round_number
        self.games = []
        
    def __str__(self):
        return f"Round {self.round_no} with {len(self.games)} games"
        
    def add_game(self, game):
        self.games.append(game)

class Season:
    def __init__(self, year):
        self.year = year
        self.rounds = []
    
    def __str__(self):
        return f"Season {self.year} - {len(self.rounds)} games"
    
    def __len__(self):
        return (len(self.rounds))
    
    def add_round(self, round):
        self.rounds.append(round)
    
    def print_round(self, round_number):
        print()
    
    def print_games(self):
        for round in self.rounds:
            for game in round.games:
                print(game)
            print('\n')
    
    
    