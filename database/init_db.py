import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT UNIQUE,
phone TEXT,
password TEXT
)
""")

# HOUSES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS houses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
house_name TEXT,
place TEXT,
price INTEGER,
rooms TEXT,
status TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS rent_due (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tenant_name TEXT,
email TEXT,
house_name TEXT,
rent_amount INTEGER,
due_date TEXT,
status TEXT
);
""")

# BOOKING TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS booking(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
phone TEXT,
place TEXT,
stay_name TEXT,
duration TEXT,
price INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully")