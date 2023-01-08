from sqlite3 import *
from mcping.util import Info

def check_table(db: Cursor, name: str) -> bool:
    db.execute(f"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='{name}'")
    return db.fetchone()[0] == 1

def create(db: Cursor):
    db.execute("CREATE TABLE Servers (Host VARCHAR(100), Software VARCHAR(100), Protocol TINYINT, Motd VARCHAR(200), MaxPlayers INT, OnlinePlayers INT,  SecureChat BOOLEAN, UpdateTime DATE , PRIMARY KEY (Host))")

def insert(db: Cursor, info: Info):
    db.execute(f"""REPLACE INTO Servers (Host, Software, Protocol, Motd, MaxPlayers, OnlinePlayers, SecureChat, UpdateTime)
              VALUES (?, ?, ?, ?, ?, ?, ?, DateTime('now'))""", (info.host, info.software, info.proto, info.motd, info.max_players, info.current_players, info.secure_chat))

def print_all(db: Cursor) -> list:
    db.execute("SELECT * FROM Servers")
    return db.fetchall()

def print_all_ordered(db: Cursor, field: str) -> list:
    db.execute(f"SELECT * FROM Servers ORDER BY {field}")
    return db.fetchall()