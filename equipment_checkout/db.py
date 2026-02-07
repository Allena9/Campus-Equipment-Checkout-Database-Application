import sqlite3

DB_FILE = "checkout.db"

def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('available','checked_out'))
    );

    CREATE TABLE IF NOT EXISTS loans (
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        checkout_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        returned_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
        FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE RESTRICT
    );

    CREATE INDEX IF NOT EXISTS idx_loans_user_id ON loans(user_id);
    CREATE INDEX IF NOT EXISTS idx_loans_item_id ON loans(item_id);
    """)
    conn.commit()

def seed_data(conn):
    users = [
        ("Alice Johnson", "alice@example.com"),
        ("Brian Lee", "brian@example.com"),
        ("Chen Wu", "chen@example.com"),
    ]
    items = [
        ("Laptop", "Computers", "available"),
        ("DSLR Camera", "Photography", "available"),
        ("Tripod", "Photography", "available"),
        ("Tablet", "Computers", "available"),
    ]

    # Safe-ish seeding: ignores duplicates by catching unique constraint
    try:
        conn.executemany("INSERT INTO users(name,email) VALUES (?,?)", users)
    except sqlite3.IntegrityError:
        pass

    try:
        conn.executemany("INSERT INTO items(name,category,status) VALUES (?,?,?)", items)
    except sqlite3.IntegrityError:
        pass

    conn.commit()
