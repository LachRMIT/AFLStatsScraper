class Player:
    def __init__(self, name, current_team):
        self.name = name
        self.current_team = current_team
    
    def __str__(self):
        return f"{self.name} - Team: {self.current_team}"