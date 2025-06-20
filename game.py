

class Game:
    def __init__(self, game_id, year, round, date, venue):
        self.game_id = game_id
        self.year = year
        self.round = round
        self.date = date
        self.venue = venue

    def __str__(self):
        return (f"Game {self.game_id}: Round {self.round} {self.year} at {self.venue} - "
                f"Home Team ID {self.home_team_id} vs Away Team ID {self.away_team_id}")

class Team:
    team_lookup = {
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
        return (f"Team Name: {self.name}, Team ID: {self.team_id}")
    
    
class Round:
    
    def __init__(self, round_no):
        self.round_no = round_no