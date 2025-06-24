class Player:
    def __init__(self, name, current_team):
        self.name = name
        self.current_team = current_team
    
    def __str__(self):
        return f"{self.name} - Team: {self.current_team}"

class Player_Stats:
    def __init__(self, player: Player, game_id: int, team: 'Team',
                kicks: int, handballs: int, disposals: int,
                goals: int, behinds: int, tackles: int):
        self.player = player
        self.game_id = game_id
        self.team = team
        self.kicks = kicks
        self.handballs = handballs
        self.disposals = disposals
        self.goals = goals
        self.behinds = behinds
        self.tackles = tackles

    def __str__(self):
        return (f"{self.player.name.ljust(20)} | "
                f"Game ID: {str(self.game_id).ljust(8)} | "
                f"Team: {self.team.name.ljust(10)} | "
                f"K: {str(self.kicks).rjust(2)} "
                f"H: {str(self.handballs).rjust(2)} "
                f"D: {str(self.disposals).rjust(2)} "
                f"G: {str(self.goals).rjust(2)} "
                f"B: {str(self.behinds).rjust(2)} "
                f"T: {str(self.tackles).rjust(2)}")
    
    def __repr__(self):
        return self.__str__()


class Game:
    FINAL_TYPE_MAP = {
        "EF": "Elimination Final",
        "SF": "Semi Final",
        "PF": "Preliminary Final",
        "GF": "Grand Final"
    }

    def __init__(self, year, round, home_team=None, away_team=None, winning_team=None, margin=None, final_type=None):
        self.game_id = None
        self.year = year
        self.round = round
        self.home_team = home_team
        self.away_team = away_team
        self.winning_team = winning_team
        self.margin = margin
        self.final_type = self.FINAL_TYPE_MAP.get(final_type, final_type)

    def set_game_id(self, id):
        self.game_id = id

    def __str__(self):
        s = f"Game {self.game_id} of Round {self.round}, {self.year}. "
        if self.home_team and self.away_team:
            s += f"{self.home_team.get_name()} v {self.away_team.get_name()}. "
        if self.winning_team:
            s += f"{self.winning_team.get_name()} won"
            if self.margin:
                s += f" by {self.margin}"
            s += ". "
        if self.final_type:
            s += f"({self.final_type})"
        return s.strip()


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
        "Western Bulldogs": 18
    }

    def __init__(self, name):
        self.name = name
        self.team_id = self.team_lookup.get(name, 99)
        
    def __str__(self):
        return f"Team Name: {self.name}, Team ID: {self.team_id}"
    
    def get_name(self):
        return self.name
    
class Round:
    
    def __init__(self, round_value, round_name: str):
        self.round_value = round_value
        self.round_name = round_name
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

class Season:
    def __init__(self, year: int):
        self.year = year
        self.rounds = []
    
    def __str__(self):
        return f"Season {self.year} - {len(self.rounds)} games"
    
    def __len__(self):
        return (len(self.rounds))
    
    def add_round(self, round):
        self.rounds.append(round)
    
    def get_round(self, round_number):
        try:
            return self.rounds[round_number-1]
        except Exception as e:
            print(f"Invalid Round Number {round_number}: {e}")
    
    def print_round(self, round_number):
        try:
            print(f"Printing Round {round_number}: ")
            for game in self.rounds[round_number-1].games:
                print(game)
        except Exception as e:
            print(f"Invalid Round Number.: {e}")
            return
    
    def print_all(self):
        for round in self.rounds:
            for game in round.games:
                print(game)
            print('\n')
    
    def num_games(self):
        return sum(len(rnd.games) for rnd in self.rounds)
