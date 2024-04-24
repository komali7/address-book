import sqlite3


def db_connect(db_name='addresses.db'):
    conn = sqlite3.connect(db_name)
    return conn

def create_addresses_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS addresses 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 latitude REAL,
                 longitude REAL,
                 address TEXT)''')
    conn.commit()