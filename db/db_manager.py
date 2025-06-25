import sqlite3
from src.models.game import *
from typing import List
from src.scraper.AFLTablesScraper import AFLTablesScraper

class AFLDBTools:
    """
    DB Population Order:
    teams -> seasons -> final_types -> rounds -> games -> players -> player_stats
    """
    def __init__(self):
        self.scraper = AFLTablesScraper()
        self.conn = sqlite3.connect('db/afl_stats.db')
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()
    
    def _table_exists(self, table_name):
        self.cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """, (table_name,))
        exists = self.cursor.fetchone() is not None
        if not exists:
            print(f"Table '{table_name}' does not exist.")
        return exists
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                current_team_id INTEGER NOT NULL,
                FOREIGN KEY (current_team_id) REFERENCES teams(team_id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS seasons (
                year INTEGER PRIMARY KEY,
                num_rounds INTEGER NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rounds (
                round_id INTEGER PRIMARY KEY AUTOINCREMENT,
                round_number TEXT NOT NULL,
                year INTEGER NOT NULL,
                FOREIGN KEY (year) REFERENCES seasons(year)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS final_types (
                final_type_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_id TEXT PRIMARY KEY,
                year INTEGER NOT NULL,
                round_id TEXT NOT NULL,
                home_team INTEGER NOT NULL,
                away_team INTEGER NOT NULL,
                final_type_id INTEGER,
                FOREIGN KEY (year) REFERENCES seasons(year),
                FOREIGN KEY (home_team) REFERENCES teams(team_id),
                FOREIGN KEY (away_team) REFERENCES teams(team_id),
                FOREIGN KEY (round_id) REFERENCES rounds(round_id),
                FOREIGN KEY (final_type_id) REFERENCES final_types(final_type_id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                game_id TEXT NOT NULL,
                team_id INTEGER NOT NULL,
                kicks INTEGER,
                handballs INTEGER,
                disposals INTEGER,
                behinds INTEGER,
                goals INTEGER,
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (game_id) REFERENCES games(game_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id)
            )
        """)

        self.conn.commit()
    
    def populate_teams(self):
        if not self._table_exists('teams'):
            return None
        
        teams = [
            (0, "The Draw"),
            (1, "Adelaide"),
            (2, "Brisbane Lions"),
            (3, "Carlton"),
            (4, "Collingwood"),
            (5, "Essendon"),
            (6, "Fremantle"),
            (7, "Geelong"),
            (8, "Gold Coast"),
            (9, "Greater Western Sydney"),
            (10, "Hawthorn"),
            (11, "Melbourne"),
            (12, "North Melbourne"),
            (13, "Port Adelaide"),
            (14, "Richmond"),
            (15, "St Kilda"),
            (16, "Sydney"),
            (17, "West Coast"),
            (18, "Western Bulldogs")
        ]
        
        for team_id, name in teams:
            self.cursor.execute("INSERT OR IGNORE INTO teams (team_id, name) VALUES (?, ?)", (team_id, name))
        self.conn.commit()
    
    def populate_season(self):
        if not self._table_exists('seasons'):
            return None
        try:
            self.cursor.execute("INSERT OR IGNORE INTO seasons (year, num_rounds) VALUES (?, ?)",
            (self.scraper.year, self.scraper.scrape_num_rounds())
            )
            
            self.conn.commit()
        except TypeError:
            print("No year set on scraper object")
            return None
        
    def populate_finals_types(self):
        if not self._table_exists('final_types'):
            return None
        
        finals_types = {
            1 : "Elimination Final",
            2 : "Qualifying Final",
            3 : "Preliminary Final",
            4 : "Semi Final",
            5 : "Grand Final"
        }
        
        for final_type_id, name in finals_types.items():
            self.cursor.execute(
                "INSERT OR IGNORE INTO final_types (final_type_id, name) VALUES (?, ?)",
                (final_type_id, name)
                )
            
            self.conn.commit()
    

if __name__ == "__main__":
    
    db = AFLDBTools()
    db.create_tables()
    
    db.scraper.set_year(1989)
    db.populate_season()
    db.close()
    