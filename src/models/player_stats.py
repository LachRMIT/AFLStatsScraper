from models.player import Player
from models.team import Team

class Player_Stats:
    def __init__(self, player: Player, game_id: int, team: Team,
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
