import sqlite3

def get_db():
    conn = sqlite3.connect("checkins.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stress_level INTEGER,
            created_at DATE DEFAULT CURRENT_DATE
        )
    """)
    db.commit()
    db.close()
