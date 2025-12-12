import sqlite3
def threadUpdate():
    conn = sqlite3.connect('userinfo.db')
    conn.execute('''
CREATE TABLE IF NOT EXISTS userinfo (
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            species TEXT,
            name TEXT,
            age INTEGER,
            disease TEXT)
'''); conn.commit()
    return conn