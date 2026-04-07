import sqlite3
import os

class Database:
    def __init__(self):
        self.db_path = os.path.join("database", "game_data.db")
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_state (
                game_state_id INTEGER PRIMARY KEY,
                current_wave INTEGER,
                objective_health INTEGER,
                upgrades TEXT,
                structures TEXT
            )
        ''')
        self.connection.commit()