import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from game import Game, Team, Round, Season
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AfltablesScraper:
    BASE_URL = "https://afltables.com/afl/"

    def __init__(self, year):
        self.year = year
        self.url = self.BASE_URL
        self.session = requests.Session()
        

    def fetch_season(self) -> str:
        season_url = f"{self.url}seas/{self.year}.html"
        print(f"\nFetching AFL season data from {self.year}")
        response = self.session.get(season_url, verify=False)
        response.raise_for_status()
        return response.text
    
    def scrape_season(self, html):
        
        season = Season(self.year)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        round_titles = soup.find_all("table", attrs={
            "style": "font: 12px Verdana;",
            "border": "2",
            "width": "100%"
        })[:25]
        
        for round_no, round_title in enumerate(round_titles, start=1):
            
            round = Round(round_no)
            
            games = round_title.find_next("table", width="100%").find("td", width="85%").find_all("table", attrs={
            "style": "font: 12px Verdana;",
            "border": "1",
            "width": "100%"
            })
            
            for id, game in enumerate(games, start=1):
                teams = game.find_all("tr")
                if len(teams) > 1:
                    home_team_text = teams[0]
                    away_team_text = teams[1]
                    
                    result_text = away_team_text.find("td", width="5%").find_next("td").text
                    if " won by " in result_text:
                        parts = result_text.split(" won by ")
                        winner = parts[0]
                        margin = parts[1].split()[0]
                    elif "Match drawn" in result_text:
                        winner = "The Draw"
                        margin = 0
                    else:
                        print("Unexpected result format:", result_text)
                    
                    home_team = Team(home_team_text.find("td", width="16%").text)
                    away_team = Team(away_team_text.find("td", width="16%").text)
                    
                    g = Game(id, self.year, (round_no+1), home_team, away_team, Team(winner), margin)
                    round.add_game(g)
                    
                    
                    
            
            season.add_round(round)
            
        return season
            
        
        
        

if __name__ == "__main__":
    scraper = AfltablesScraper(year=2024)
    html = scraper.fetch_season()
    season = scraper.scrape_season(html)
    print(season)
    season.print_games()
