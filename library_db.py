import sqlite3
import os

#  Create "database" folder if it does not exist
if not os.path.exists("database"):
    os.makedirs("database")

#  Path to the SQLite database
db_path = "database/library.db"

#  Create or open the database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# ---------------------------------------------------
# Users Table
# ---------------------------------------------------
c.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    created_at TEXT
);
""")

# ---------------------------------------------------
# Books Table
# ---------------------------------------------------
c.execute("""
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    publisher TEXT,
    publish_year INTEGER,
    price REAL,
    stock INTEGER,
    rating REAL,
    description TEXT
);
""")

# ---------------------------------------------------
#  Sales Table
# ---------------------------------------------------
c.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    sale_date TEXT
);
""")

# ---------------------------------------------------
#  Reviews Table
# ---------------------------------------------------
c.execute("""
CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    rating INTEGER,
    comment TEXT,
    created_at TEXT
);
""")

# ---------------------------------------------------
#  Statistics Table
# ---------------------------------------------------
c.execute("""
CREATE TABLE IF NOT EXISTS Statistics (
    book_id INTEGER PRIMARY KEY,
    total_sales INTEGER DEFAULT 0,
    average_rating REAL DEFAULT 0,
    FOREIGN KEY (book_id) REFERENCES Books(id)
);
""")

#  Save changes and close connection
conn.commit()
conn.close()

print(" Database created successfully inside the 'database' folder!")
