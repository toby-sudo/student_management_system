import mysql.connector
from mysql.connector import errorcode

HOST = "localhost"
USER = "root"          # change to your MySQL username
PASSWORD = "password"  # change to your MySQL password

DB_NAME = "sms_db"

TABLE_STUDENTS = (
    "CREATE TABLE IF NOT EXISTS students ("
    "  id INT PRIMARY KEY AUTO_INCREMENT,"
    "  name VARCHAR(100) NOT NULL,"
    "  email VARCHAR(100) UNIQUE,"
    "  branch VARCHAR(50),"
    "  year INT"
    ") ENGINE=InnoDB"
)

def get_conn(db=None):
    cfg = dict(host=HOST, user=USER, password=PASSWORD)
    if db:
        cfg["database"] = db
    return mysql.connector.connect(**cfg)

def init_db():
    cnx = get_conn()
    cursor = cnx.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cnx.database = DB_NAME
        cursor.execute(TABLE_STUDENTS)
        cnx.commit()
        print("[OK] Database and table ready.")
    finally:
        cursor.close()
        cnx.close()

def add_student():
    name = input("Name: ")
    email = input("Email: ")
    branch = input("Branch: ")
    year = int(input("Year: "))
    cnx = get_conn(DB_NAME)
    cur = cnx.cursor()
    cur.execute("INSERT INTO students (name, email, branch, year) VALUES (%s,%s,%s,%s)",
                (name, email, branch, year))
    cnx.commit()
    print("[OK] Student added with id =", cur.lastrowid)
    cur.close(); cnx.close()

def update_student():
    sid = int(input("Student ID to update: "))
    name = input("Name (leave blank to skip): ")
    email = input("Email (leave blank to skip): ")
    branch = input("Branch (leave blank to skip): ")
    year = input("Year (leave blank to skip): ")

    sets, vals = [], []
    if name: sets.append("name=%s"); vals.append(name)
    if email: sets.append("email=%s"); vals.append(email)
    if branch: sets.append("branch=%s"); vals.append(branch)
    if year: sets.append("year=%s"); vals.append(int(year))

    if not sets:
        print("No updates provided."); return

    vals.append(sid)
    cnx = get_conn(DB_NAME)
    cur = cnx.cursor()
    cur.execute(f"UPDATE students SET {', '.join(sets)} WHERE id=%s", tuple(vals))
    cnx.commit()
    print(f"[OK] {cur.rowcount} row(s) updated.")
    cur.close(); cnx.close()

def delete_student():
    sid = int(input("Student ID to delete: "))
    cnx = get_conn(DB_NAME)
    cur = cnx.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (sid,))
    cnx.commit()
    print(f"[OK] {cur.rowcount} row(s) deleted.")
    cur.close(); cnx.close()

def search_student():
    sid = int(input("Student ID to search: "))
    cnx = get_conn(DB_NAME)
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE id=%s", (sid,))
    row = cur.fetchone()
    if row:
        print(row)
    else:
        print("Not found.")
    cur.close(); cnx.close()

def list_students():
    cnx = get_conn(DB_NAME)
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM students ORDER BY id")
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close(); cnx.close()

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
===== Student Management System (MySQL) =====
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
