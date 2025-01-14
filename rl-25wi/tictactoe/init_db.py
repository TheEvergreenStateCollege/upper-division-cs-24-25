import sqlite3

connection = sqlite3.connect("database.db")

with open("matches.sql") as f:
    connection.executescript(f.read())
cur = connection.cursor()
cur.execute("INSERT INTO matches (matchID) VALUES(?)", (["s0NlC"]))
connection.commit()
connection.close()

connection = sqlite3.connect("database.db")

with open("boards.sql") as f:
    connection.executescript(f.read())
cur = connection.cursor()
cur.execute(
    "INSERT INTO boards (index0, index1, index2, index3, index4, index5, index6, index7, index8, match) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
)
connection.commit()
connection.close()
