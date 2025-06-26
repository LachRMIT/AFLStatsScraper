import sqlite3
from src.models import *
from typing import List
from src.scraper.AFLTablesScraper import AFLTablesScraper
import time
import logging

class AFLDBTools:
    """
    DB Population Order:
    teams -> seasons -> final_types -> rounds -> games -> players -> player_stats
    """
    def __init__(self):
        self.scraper = AFLTablesScraper()
        self.conn = sqlite3.connect('db/afl_stats.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
    
    def __del__(self):
        self.close()
    
    def close(self):
        self.conn.close()
    
    def tables_count(self):
        self.cursor.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%';
        """)
        return self.cursor.fetchone()[0]

    def verify_tables(self):
        with open("db/schema.sql", "r", encoding="utf-8") as f:
            content = f.read()
        create_statements = content.upper().count("CREATE TABLE")
        
        if self.tables_count() != create_statements:
            logging.error("Incorrect number of tables detected.")
            self.drop_tables()
            self.create_tables()
    
    def _table_exists(self, table_name):
        self.cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """, (table_name,))
        exists = self.cursor.fetchone() is not None
        if not exists:
            logging.error(f"Table '{table_name}' does not exist.")
        return exists
    
    def create_tables(self):
        with open("db/schema.sql", "r", encoding="utf-8") as f:
            schema_sql = f.read()
            self.cursor.executescript(schema_sql)
            logging.info("Created tables if not existing.")
        self.conn.commit()
    
    def drop_tables(self):
        tables = [
            "player_stats",
            "games",
            "final_types",
            "rounds",
            "seasons",
            "players",
            "teams"
        ]

        check = input("Type y to confirm DROPPING ALL tables: ")
        if check != "y":
            logging.info("Left tables alone.")
            return None
        
        for table in tables:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table};")
            logging.info(f"DROPPED TABLE IF EXISTED {table}")
        
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
    
    def populate_season(self, season: Season):
        if not self._table_exists('seasons'):
            return None
        try:
            self.cursor.execute("INSERT OR IGNORE INTO seasons (year, num_rounds) VALUES (?, ?)",
            (season.year, len(season)))
            self.conn.commit()
            logging.info(f"Inserted Season {season.year}, Number of Games: {season.num_games()}")
        except Exception as e:
            logging.error(f"Failed to populate Season {season.year}: {e}")
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
        try:
            for final_type_id, name in finals_types.items():
                self.cursor.execute(
                    "INSERT OR IGNORE INTO final_types (final_type_id, name) VALUES (?, ?)",
                    (final_type_id, name)
                    )
                
                self.conn.commit()
            logging.info("Inserted all finals types.")
        except Exception as e:
            logging.error(f"Failed to insert finals types:  {e}")
            return None
            
    def populate_game(self, game: Game):
        if not self._table_exists('games'):
            return None
        try:
            self.cursor.execute("""
            INSERT OR IGNORE INTO games (game_id, year, round_value, home_team_id, away_team_id, winning_team_id, margin, final_type_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (game.game_id, game.year, game.round, game.home_team.team_id, game.away_team.team_id, game.winning_team.team_id, game.margin, Finals_Types(game.final_type).id))
            self.conn.commit()
        except Exception as e:
            logging.error(f"Failed to populate Game : {e}")
            return None
    
    def populate_round(self, round: Round):
        if not self._table_exists('rounds'):
            return None
        try:
            self.cursor.execute("INSERT OR IGNORE INTO rounds (round_value, year) VALUES (?, ?)",
            (round.round_value, round.round_year))
            self.conn.commit()
            logging.info(f"Inserted Round {round.round_value}, {round.round_year}")
        except Exception as e:
            logging.error(f"Failed to populate Round {round.round_value}: {e}")
            return None
    
    def populate_rounds_from_season(self, season: Season):
        for round in season.rounds:
            self.populate_round(round)
    
    def populate_games_from_season(self, season: Season):
        for round in season.rounds:
            for game in round.games:
                try:
                    self.populate_game(game)
                except Exception as e:
                    logging.error(f"Error with {game}: {e}")
    
    def populate_player(self, player: Player):
        
        return None
    
    def populate_db(self) -> None:
        check = input("Are you sure you want to populate the whole database?\nY / N: ")
        if check.lower() != "y":
            logging.info("NO selected. Exiting...")
            return None
        
        self.verify_tables()
        
        self.populate_teams()

        for i in range (1897, 2026):
            self.scraper.set_year(i)
            try:
                season = self.scraper.scrape_season()
                self.populate_season(season)
                self.populate_rounds_from_season(season)
                self.populate_games_from_season(season)
            except Exception as e:
                logging.error(f"Error with Season {i} : {e}")
            time.sleep(0.1)
        self.populate_finals_types()
        
    
        
