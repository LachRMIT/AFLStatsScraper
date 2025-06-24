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

