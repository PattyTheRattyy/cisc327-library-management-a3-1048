import sqlite3

conn = sqlite3.connect("library.db")
conn.row_factory = sqlite3.Row

print("=== TABLES ===")
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
for t in tables:
    print("-", t["name"])

print("\n=== BOOKS ===")
books = conn.execute("SELECT * FROM books").fetchall()
for b in books:
    print(dict(b))

print("\n=== BORROW RECORDS ===")
records = conn.execute("SELECT * FROM borrow_records").fetchall()
for r in records:
    print(dict(r))

conn.close()
