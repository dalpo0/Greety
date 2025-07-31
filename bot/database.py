import sqlite3
from datetime import datetime

class UserDatabase:
    def __init__(self, db_path='greety.db'):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    chat_id INTEGER,
                    latitude REAL,
                    longitude REAL,
                    join_date TEXT
                )""")

    def log_join(self, user_id, username, first_name, chat_id):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, NULL, NULL, ?)",
                (user_id, username, first_name, chat_id, datetime.now().isoformat())
            )

    def update_location(self, user_id, lat, lng):
        with self.conn:
            self.conn.execute(
                "UPDATE users SET latitude = ?, longitude = ? WHERE user_id = ?",
                (lat, lng, user_id)
            )
