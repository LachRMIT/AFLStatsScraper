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