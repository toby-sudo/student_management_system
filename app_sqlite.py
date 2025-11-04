import sqlite3, os

DB_FILE = "sms.sqlite3"

def get_conn():
    return sqlite3.connect(DB_FILE)

def init_db():
    with get_conn() as cnx:
        cnx.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            branch TEXT,
            year INTEGER
        )""")
    print("[OK] Database and table ready.")

def add_student():
    name = input("Name: ")
    email = input("Email: ")
    branch = input("Branch: ")
    year = int(input("Year: "))
    with get_conn() as cnx:
        cur = cnx.execute("INSERT INTO students (name, email, branch, year) VALUES (?,?,?,?)",
                          (name, email, branch, year))
        print("[OK] Student added with id =", cur.lastrowid)

def update_student():
    sid = int(input("Student ID to update: "))
    name = input("Name (leave blank to skip): ")
    email = input("Email (leave blank to skip): ")
    branch = input("Branch (leave blank to skip): ")
    year = input("Year (leave blank to skip): ")

    sets, vals = [], []
    if name: sets.append("name=?"); vals.append(name)
    if email: sets.append("email=?"); vals.append(email)
    if branch: sets.append("branch=?"); vals.append(branch)
    if year: sets.append("year=?"); vals.append(int(year))

    if not sets:
        print("No updates provided."); return

    vals.append(sid)
    with get_conn() as cnx:
        cur = cnx.execute(f"UPDATE students SET {', '.join(sets)} WHERE id=?", tuple(vals))
        print(f"[OK] {cur.rowcount} row(s) updated.")

def delete_student():
    sid = int(input("Student ID to delete: "))
    with get_conn() as cnx:
        cur = cnx.execute("DELETE FROM students WHERE id=?", (sid,))
        print(f"[OK] {cur.rowcount} row(s) deleted.")

def search_student():
    sid = int(input("Student ID to search: "))
    with get_conn() as cnx:
        cur = cnx.execute("SELECT * FROM students WHERE id=?", (sid,))
        row = cur.fetchone()
        print(row if row else "Not found.")

def list_students():
    with get_conn() as cnx:
        cur = cnx.execute("SELECT * FROM students ORDER BY id")
        for r in cur.fetchall():
            print(r)

def menu():
    init_db()
    actions = {
        "1": add_student,
        "2": update_student,
        "3": delete_student,
        "4": search_student,
        "5": list_students,
        "0": exit
    }
    while True:
        print("""
===== Student Management System (SQLite) =====
1) Add Student
2) Update Student
3) Delete Student
4) Search Student
5) List Students
0) Exit
""")
        choice = input("Select: ").strip()
        action = actions.get(choice)
        if action: action()
        else: print("Invalid choice.")

if __name__ == "__main__":
    menu()
