import sqlite3
from datetime import date, timedelta

# -------- READ (Queries) --------
def list_users(conn):
    rows = conn.execute("SELECT user_id, name, email FROM users ORDER BY name").fetchall()
    print("\nUsers:")
    for r in rows:
        print(f"  {r['user_id']:>3} | {r['name']:<18} | {r['email']}")
    if not rows:
        print("  (none)")

def list_items(conn, only_available=False):
    if only_available:
        rows = conn.execute("""
            SELECT item_id, name, category, status
            FROM items
            WHERE status='available'
            ORDER BY category, name
        """).fetchall()
    else:
        rows = conn.execute("""
            SELECT item_id, name, category, status
            FROM items
            ORDER BY category, name
        """).fetchall()

    print("\nItems:")
    for r in rows:
        print(f"  {r['item_id']:>3} | {r['name']:<20} | {r['category']:<12} | {r['status']}")
    if not rows:
        print("  (none)")

def search_items(conn, term):
    rows = conn.execute("""
        SELECT item_id, name, category, status
        FROM items
        WHERE name LIKE ? OR category LIKE ?
        ORDER BY category, name
    """, (f"%{term}%", f"%{term}%")).fetchall()

    print("\nSearch results:")
    for r in rows:
        print(f"  {r['item_id']:>3} | {r['name']:<20} | {r['category']:<12} | {r['status']}")
    if not rows:
        print("  (none)")

def list_active_loans(conn):
    rows = conn.execute("""
        SELECT l.loan_id, u.name AS user_name, i.name AS item_name,
               l.checkout_date, l.due_date
        FROM loans l
        JOIN users u ON u.user_id = l.user_id
        JOIN items i ON i.item_id = l.item_id
        WHERE l.returned_date IS NULL
        ORDER BY l.due_date
    """).fetchall()

    print("\nActive loans:")
    for r in rows:
        print(f"  Loan {r['loan_id']:>3} | {r['user_name']:<15} | {r['item_name']:<20} | due {r['due_date']}")
    if not rows:
        print("  (none)")

# -------- CREATE (Insert) --------
def add_user(conn, name, email):
    conn.execute("INSERT INTO users(name,email) VALUES (?,?)", (name, email))
    conn.commit()
    print("User added.")

def add_item(conn, name, category):
    conn.execute("INSERT INTO items(name,category,status) VALUES (?,?, 'available')", (name, category))
    conn.commit()
    print("Item added.")

def checkout_item(conn, user_id, item_id, days=7):
    item = conn.execute("SELECT status FROM items WHERE item_id=?", (item_id,)).fetchone()
    if not item:
        print("No such item.")
        return
    if item["status"] != "available":
        print("Item is not available.")
        return

    user = conn.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,)).fetchone()
    if not user:
        print("No such user.")
        return

    today = date.today().isoformat()
    due = (date.today() + timedelta(days=days)).isoformat()

    conn.execute("""
        INSERT INTO loans(user_id,item_id,checkout_date,due_date,returned_date)
        VALUES (?,?,?,?,NULL)
    """, (user_id, item_id, today, due))
    conn.execute("UPDATE items SET status='checked_out' WHERE item_id=?", (item_id,))
    conn.commit()
    print("Checkout created.")

# -------- UPDATE --------
def return_loan(conn, loan_id):
    loan = conn.execute("""
        SELECT item_id, returned_date
        FROM loans
        WHERE loan_id=?
    """, (loan_id,)).fetchone()

    if not loan:
        print("No such loan.")
        return
    if loan["returned_date"] is not None:
        print("Loan already returned.")
        return

    today = date.today().isoformat()
    conn.execute("UPDATE loans SET returned_date=? WHERE loan_id=?", (today, loan_id))
    conn.execute("UPDATE items SET status='available' WHERE item_id=?", (loan["item_id"],))
    conn.commit()
    print("Loan returned (updated).")

def update_item_name(conn, item_id, new_name):
    cur = conn.execute("UPDATE items SET name=? WHERE item_id=?", (new_name, item_id))
    conn.commit()
    if cur.rowcount == 0:
        print("No such item.")
    else:
        print("Item updated.")

# -------- DELETE --------
def delete_loan(conn, loan_id):
    cur = conn.execute("DELETE FROM loans WHERE loan_id=?", (loan_id,))
    conn.commit()
    print("Loan deleted." if cur.rowcount else "No such loan.")

def delete_item(conn, item_id):
    row = conn.execute("SELECT status FROM items WHERE item_id=?", (item_id,)).fetchone()
    if not row:
        print("No such item.")
        return
    if row["status"] != "available":
        print("Cannot delete: item is checked out.")
        return

    cur = conn.execute("DELETE FROM items WHERE item_id=?", (item_id,))
    conn.commit()
    print("Item deleted." if cur.rowcount else "No such item.")

def delete_user(conn, user_id):
    active = conn.execute("""
        SELECT 1 FROM loans
        WHERE user_id=? AND returned_date IS NULL
        LIMIT 1
    """, (user_id,)).fetchone()
    if active:
        print("Cannot delete: user has an active loan.")
        return

    cur = conn.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    print("User deleted." if cur.rowcount else "No such user.")
