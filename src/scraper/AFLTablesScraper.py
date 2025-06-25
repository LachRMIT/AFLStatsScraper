from typing import List
import re
import requests
from bs4 import BeautifulSoup

from src.models import Game, Team, Round, Season, Player_Stats, Player

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AFLTablesScraper:
    BASE_URL = "https://afltables.com/afl/"
    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    }

    def __init__(self):
        self.url = self.BASE_URL
        self.current_url = None
        self.session = requests.Session()

        self.year = None
        self.current_player = None
        self.current_player_years = []

    def set_year(self, year):
        self.year = year
    
    def fetch_season(self) -> str:
        if not self.year:
            print("No year selected.")
            return None
        season_url = f"{self.url}seas/{self.year}.html"
        self.current_url = season_url
        print(f"\nFetching AFL season data from {self.year}")
        try:
            response = self.session.get(season_url, verify=False, headers=self.HEADERS)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"No Season data found for {self.year}: {e}")
            return None
        
    def fetch_stats(self, name: str) -> str:
        self.current_player = name
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1]
        stat_url = f"{self.url}stats/players/{name[0].capitalize()}/{first_name}_{last_name}.html"
        print(stat_url)

        print(f"\nFetching AFL stats data for {name}")
        try:
            response = self.session.get(stat_url, verify=False, headers=self.HEADERS)
            response.raise_for_status()
            return response.text
            
        except Exception as e:
            print(f"No stats found for {name}")
            return None
        
    def scrape_season(self) -> Season:
        html = self.fetch_season()
        
        if not html:
            print(f"No Season data found for {self.year}")
            return None
        
        season = Season(self.year)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all relevant tables
        all_tables = soup.find_all("table", attrs={
            "style": "font: 12px Verdana;",
            "border": "2",
            "width": "100%"
        })
        
        
        round_tables = [table for table in all_tables if "round" in table.get_text().lower()]
        num_rounds = int(round_tables[-1].text.split("Round ")[1].split("Rnd")[0])
        # season_num_games = soup.find("td", colspan="12").text.split("Games: ")[1].split(",")[0]
        
        for round_no, round_table in enumerate(round_tables, start=1):
            try:
                round_name = round_table.find_next().get_text().strip().lower()
                round = Round(round_no, round_name, self.year)
                
                games_table = round_table.find_next("table", width="100%").find("td", width="85%")
                games = games_table.find_all("table") if games_table else []
                
                self._scrape_games(games, round)
                
                if len(round) > 0:
                    season.add_round(round)
                    
            except IndexError as e:
                print(f"Index error on Round {round_no}: {e}")
            except Exception as e:
                print(f"Error processing round {round_no}: {e}")
                import traceback
                traceback.print_exc()
                return None
        
        finals_games = soup.find("a", attrs={"name": "fin"}).find_next("table").find_all_next("table", attrs={
            "style": "font: 12px Verdana;",
            "border": "1",
            "width": "100%"
        })
        
        finals_grouped = {}
        
        for game_table in finals_games:
            header = game_table.find_previous("b")
            if not header:
                continue
            final_type = header.text.strip()
            if final_type not in finals_grouped:
                finals_grouped[final_type] = []
            finals_grouped[final_type].append(game_table)
        
        for final_type, game_tables in finals_grouped.items():
            round_id = ''.join(word[0] for word in final_type.split()).upper()
            round_obj = Round(round_id, final_type, self.year)
            self._scrape_games(game_tables, round_obj, is_finals=True)
            if len(round_obj) > 0:
                season.add_round(round_obj)
        
        print(f"Successfully scraped.")
        
        # if season.num_games() != int(season_num_games):
        #     print("ERROR: Missing Games!")
        
        return season

    def _scrape_games(self, games: list, round: Round, is_finals: bool = False):
        for game_id, game_table in enumerate(games, start=1):
            try:
                teams = game_table.find_all("tr")
                if len(teams) < 2:
                    continue
                
                home_team_row, away_team_row = teams[0], teams[1]
                
                result_text = away_team_row.find("td", width="5%").find_next("td").text
                if " won by " in result_text:
                    parts = result_text.split(" won by ")
                    winner = parts[0]
                    margin = parts[1].split()[0]
                elif "Match drawn" in result_text:
                    winner = "The Draw"
                    margin = 0
                else:
                    continue
                
                home_team = Team(home_team_row.find("td", width="16%").text)
                away_team = Team(away_team_row.find("td", width="16%").text)
                
                final_type = None
                if is_finals:
                    final_type_element = game_table.find_previous("b")
                    final_type = final_type_element.text if final_type_element else None
                
                game = Game(self.year, round.round_value, home_team, away_team, Team(winner), margin, final_type)
                game.set_game_id(game_id)
                round.add_game(game)
                
            except Exception as e:
                print(f"Error parsing game {home_team} v {away_team} in round {round.round_value}: {e}")
                continue
    
    def scrape_stats(self, html: str) -> List[Player_Stats]:
        def safe_int(tag):
            text = tag.text.strip()
            return int(text) if text.isdigit() else 0
        
        if not html:
            print(f"No Stats data found")
            return None
        if not self.year:
            print(f"No year selected for fetching.")
            return None
        if not self.current_player:
            print(f"No current player selected in object.")
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        tables = soup.find_all("a", attrs={
            "name": re.compile(r"^\d{5}$")
        })

        season_stats = []
        for table in tables:
            year_split = table.get("name")[:-1]
            if len(year_split) == 4 and int(year_split) == self.year:
                year = table
        try:
            games_played = year.find_next("table", border="2", style="font: 12px Verdana;").find_next("tbody").find_all("tr", recursive=False)
        except UnboundLocalError as u:
            print(f"No data found for {self.current_player} in Season {self.year}")
            return None
        for game in games_played:
            game_stats = game.find_all("td")
            
            # game_num = self._get_game_number()
            
            round_value = game_stats[2].text.strip()
            curr_team = game.parent.find_previous_sibling("thead").get_text(strip=True).split(" - ")[0]
            game_id = f"{round_value}{self.year}" if len(round_value) == 2 else f"0{round_value}{self.year}"
            player_stats = Player_Stats(
                Player(soup.find("h1").text, curr_team),
                game_id,
                Team(curr_team),
                safe_int(game_stats[5]),
                safe_int(game_stats[7]),
                safe_int(game_stats[8]),
                safe_int(game_stats[9]),
                safe_int(game_stats[10]),
                safe_int(game_stats[12])
            )
            
            season_stats.append(player_stats)
        return season_stats
    
    def scrape_num_rounds(self) -> int:
        season_html = self.fetch_season()
        soup = BeautifulSoup(season_html, 'html.parser')
        
        all_tables = soup.find_all("table", attrs={
            "style": "font: 12px Verdana;",
            "border": "2",
            "width": "100%"
        })
        
        round_tables = [table for table in all_tables if "round" in table.get_text().lower()]
        finals_table = next((table for table in all_tables if "finals" in table.get_text().lower()), None)
        
        num_rounds = int(round_tables[-1].text.split("Round ")[1].split("Rnd")[0])
        
        finals = []
        finals_games = finals_table.find_all_next("table", attrs={
            "style": "font: 12px Verdana;",
            "border": "2",
            "width": "100%"
        })
        
        for final in finals_games:
            finals.append(final.text)
            
        finals_rounds = len(set(finals))

        return (num_rounds + finals_rounds)
        
        
        
if __name__ == "__main__":

    scraper = AFLTablesScraper()
    scraper.set_year(2024)
    season = scraper.scrape_season()
    print(season)
