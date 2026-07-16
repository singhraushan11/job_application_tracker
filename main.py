#Job Application Tracker :-

import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


# connection with database:-
def get_con():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# User input:-
def get_input(msg):
    while True:
        val = input(f"Enter {msg}: ")
        if val == "":
            print("Input cannot be empty!")
        else:
            return val


def get_date():
    while True:
        dt = input("Enter applied date (YYYY-MM-DD): ")
        try:
            datetime.strptime(dt, "%Y-%m-%d")
            return dt
        except ValueError:
            print("Wrong date format!")


def get_status():
    st = ["applied", "interview", "offer", "rejected", "selected"]

    print("\nSelect Status")
    for i in range(len(st)):
        print(f"{i+1}. {st[i]}")

    while True:
        ch = input("Enter choice: ")
        if ch.isdigit() and 1 <= int(ch) <= len(st):
            return st[int(ch)-1]
        else:
            print("Wrong choice!")


# CRUD operations :-
def add_application(com, rl, dt, st="applied", nt=""):
    con = get_con()
    cur = con.cursor()

    if nt == "":
        nt = None

    q = """
    INSERT INTO applications
    (company_name, role, applied_date, status, notes)
    VALUES (%s,%s,%s,%s,%s)
    """

    cur.execute(q, (com, rl, dt, st, nt))
    con.commit()

    print("Application Added")
    print("ID :", cur.lastrowid)

    cur.close()
    con.close()


def view_application():
    con = get_con()
    cur = con.cursor()

    cur.execute("SELECT * FROM applications")
    res = cur.fetchall()

    print_application(res)

    cur.close()
    con.close()


def update_application(id, st):
    con = get_con()
    cur = con.cursor()

    q = "UPDATE applications SET status=%s WHERE id=%s"

    cur.execute(q, (st, id))
    con.commit()

    if cur.rowcount == 0:
        print("ID not found.")
    else:
        print("Status Updated.")

    cur.close()
    con.close()


def del_application(id):
    con = get_con()
    cur = con.cursor()

    q = "DELETE FROM applications WHERE id=%s"

    cur.execute(q, (id,))
    con.commit()

    if cur.rowcount == 0:
        print("ID not found.")
    else:
        print("Deleted Successfully.")

    cur.close()
    con.close()

#  function :-
def print_application(rows):
    if not rows:
        print("No Data Found.")
        return

    for r in rows:
        print(f"ID: {r[0]}, Company: {r[1]}, Role: {r[2]}, Date: {r[3]}, Status: {r[4]}, Notes: {r[5]}")


def get_application(id):
    con = get_con()
    cur = con.cursor()

    q = "SELECT * FROM applications WHERE id=%s"
    cur.execute(q, (id,))
    res = cur.fetchone()

    cur.close()
    con.close()

    return res


# Search applications :-
def search_application(ch, key):
    con = get_con()
    cur = con.cursor()

    col = {
        "1": "company_name",
        "2": "role"
    }

    q = f"SELECT * FROM applications WHERE {col[ch]} LIKE %s"

    cur.execute(q, (f"%{key}%",))
    res = cur.fetchall()

    print(f"\nFound {len(res)} Result(s)")
    print_application(res)

    cur.close()
    con.close()

# Menu :-
def main():

    while True:

        print("\n***** JOB APPLICATION TRACKER *****")
        print("1. Add Application")
        print("2. View Applications")
        print("3. Search")
        print("4. Update Status")
        print("5. Delete")
        print("6. Exit")

        ch = input("Enter Choice : ")

        try:

            if ch == "1":
                com = get_input("Company Name")
                rl = get_input("Role")
                dt = get_date()
                st = get_status()
                nt = input("Enter Notes : ")

                add_application(com, rl, dt, st, nt)

            elif ch == "2":
                view_application()

            elif ch == "3":
                print("\nSearch By")
                print("1. Company")
                print("2. Role")

                f = input("Enter Choice : ")

                if f in ["1", "2"]:
                    key = get_input("Keyword")
                    search_application(f, key)
                else:
                    print("Wrong Choice")


            elif ch == "4":
                id = int(input("Enter ID : "))
                app = get_application(id)

                if app:
                    print(f"\n{app[1]} - {app[2]}")
                    c = input("Update ? (y/n) : ").lower()

                    if c == "y":
                        st = get_status()
                        update_application(id, st)
                else:
                    print("ID Not Found")

            elif ch == "5":

                id = int(input("Enter ID : "))
                app = get_application(id)

                if app:
                    print(f"\n{app[1]} - {app[2]}")
                    c = input("Delete ? (y/n) : ").lower()

                    if c == "y":
                        del_application(id)
                else:
                    print("ID Not Found")

            elif ch == "6":

                print("Good Bye")
                break

            else:

                print("Wrong Choice")

        except Exception as e:
                print("Error:", e)

main()