class Season:
    
    def __init__(self, year: int):
        self.year = year
        self.rounds = []
    
    def __str__(self):
        return f"Season {self.year} - {len(self.rounds)} rounds"
    
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