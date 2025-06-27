PRAGMA foreign_keys = ON;

-- Teams
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Players
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    current_team_id INTEGER NOT NULL,
    date_of_birth TEXT NOT NULL,
    height INTEGER,
    weight INTEGER,
    UNIQUE (name, current_team_id, date_of_birth)
    FOREIGN KEY (current_team_id) REFERENCES teams(team_id)
);

-- Seasons
CREATE TABLE IF NOT EXISTS seasons (
    year INTEGER PRIMARY KEY,
    num_rounds INTEGER NOT NULL
);

-- Rounds
CREATE TABLE IF NOT EXISTS rounds (
    round_value TEXT NOT NULL,
    year INTEGER NOT NULL,
    PRIMARY KEY (round_value, year),
    FOREIGN KEY (year) REFERENCES seasons(year)
);

-- Final Types
CREATE TABLE IF NOT EXISTS final_types (
    final_type_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Games
CREATE TABLE IF NOT EXISTS games (
    game_id TEXT PRIMARY KEY,
    year INTEGER NOT NULL,
    round_value TEXT NOT NULL,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    winning_team_id INTEGER NOT NULL,
    margin INTEGER NOT NULL,
    final_type_id INTEGER,
    FOREIGN KEY (year) REFERENCES seasons(year),
    FOREIGN KEY (round_value, year) REFERENCES rounds(round_value, year),
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (winning_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (final_type_id) REFERENCES final_types(final_type_id)
);

-- Player Stats
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
);
