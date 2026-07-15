import mysql.connector
from dotenv import load_dotenv      
import os                           
from datetime import datetime       

load_dotenv()                        


# ---- DATABASE CONNECTION ----
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# ---- INPUT VALIDATION ----

def get_non_empty_input(field_name):
    while True:
        value = input(f"Enter {field_name}: ").strip()
        if value == "":
            print(f"{field_name} cannot be empty! Please try again.")
        else:
            return value


def get_valid_date():
    while True:
        date_str = input("Enter applied date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD (e.g., 2026-07-12).")


def get_valid_status():
    statuses = ["applied", "interview", "offer", "rejected", "selected"]
    print("\nSelect status:")
    for i, s in enumerate(statuses, start=1):
        print(f"{i}. {s}")

    while True:
        choice = input(f"Enter choice (1-{len(statuses)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(statuses):
            return statuses[int(choice) - 1]
        else:
            print(f"Invalid choice! Please enter a number between 1-{len(statuses)}.")


# ---- CRUD FUNCTIONS ----

def add_application(company, role, applied_date, status="applied", notes=""):
    conn = get_connection()
    cursor = conn.cursor()

    notes_value = notes.strip() if notes.strip() != "" else None

    query = """
        INSERT INTO applications (company_name, role, applied_date, status, notes)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (company, role, applied_date, status, notes_value)

    cursor.execute(query, values)
    conn.commit()

    print(f"Application added: {company} - {role} (ID: {cursor.lastrowid})")

    cursor.close()
    conn.close()


def view_applications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")
    result = cursor.fetchall()
    print_applications(result)

    cursor.close()
    conn.close()

def update_status(application_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE applications SET status = %s WHERE id = %s"
    cursor.execute(query, (new_status, application_id))
    conn.commit()

    if cursor.rowcount == 0:
        print(f"No application found with ID {application_id}.")
    else:
        print(f"Status updated successfully for ID {application_id} to {new_status}.")

    cursor.close()
    conn.close()


def delete_application(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM applications WHERE id = %s"
    cursor.execute(query, (application_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print(f"No application found with ID {application_id}.")
    else:
        print(f"Application with ID {application_id} deleted successfully.")

    cursor.close()
    conn.close()


# ---- HELPER FUNCTIONS ----
def print_applications(rows):
    if not rows:
        print("No applications found.")
        return
    for row in rows:
        print(f"ID: {row[0]}, Company: {row[1]}, Role: {row[2]}, Applied Date: {row[3]}, Status: {row[4]}, Notes: {row[5]}")


def get_application_by_id(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE id = %s", (application_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

# --- SEARCH ---
def search_applications(field, keyword):
    conn = get_connection()
    cursor = conn.cursor()

    column_map = {
        "1": "company_name",
        "2": "role",
        "3": "status"
    }
    column = column_map[field]

    query = f"SELECT * FROM applications WHERE {column} LIKE %s"
    cursor.execute(query, (f"%{keyword}%",))
    result = cursor.fetchall()

    print(f"\nFound {len(result)} result(s):")
    print_applications(result)

    cursor.close()
    conn.close()

# --- SORT ---
def sort_applications(order_choice):
    conn = get_connection()
    cursor = conn.cursor()

    if order_choice == "1":
        query = "SELECT * FROM applications ORDER BY applied_date DESC"   # newest first
    elif order_choice == "2":
        query = "SELECT * FROM applications ORDER BY applied_date ASC"    # oldest first
    else:
        query = "SELECT * FROM applications ORDER BY company_name ASC"    # A to Z

    cursor.execute(query)
    result = cursor.fetchall()
    print_applications(result)

    cursor.close()
    conn.close()

# --- STATISTICS ---
def show_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT status, COUNT(*) FROM applications GROUP BY status")
    status_counts = cursor.fetchall()

    print("\n===== STATISTICS DASHBOARD =====")
    print(f"Total Applications: {total}")
    for status, count in status_counts:
        print(f"{status.capitalize()}: {count}")

    cursor.close()
    conn.close()


# ---- MAIN MENU ----
def main_menu():
    while True:
        print("\n===== JOB APPLICATION TRACKER =====")
        print("1. Add Application")
        print("2. View All Applications")
        print("3. Search Application")
        print("4. Sort Applications")
        print("5. Statistics Dashboard")
        print("6. Update Application Status")
        print("7. Delete Application")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        try:
            if choice == "1":
                company = get_non_empty_input("company name")
                role = get_non_empty_input("role")
                applied_date = get_valid_date()
                status = get_valid_status()
                notes = input("Enter notes (optional): ")
                add_application(company, role, applied_date, status=status, notes=notes)

            elif choice == "2":
                view_applications()

            elif choice == "3":
                print("\nSearch by:")
                print("1. Company Name")
                print("2. Role")
                print("3. Status")
                field = input("Enter choice (1-3): ").strip()
                if field in ["1", "2", "3"]:
                    keyword = get_non_empty_input("search keyword")
                    search_applications(field, keyword)
                else:
                    print("Invalid choice.")

            elif choice == "4":
                print("\nSort by:")
                print("1. Newest First")
                print("2. Oldest First")
                print("3. Company Name (A-Z)")
                order_choice = input("Enter choice (1-3): ").strip()
                sort_applications(order_choice)

            elif choice == "5":
                show_statistics()

            elif choice == "6":
                app_id = int(input("Enter application ID: "))
                app = get_application_by_id(app_id)
                if app is None:
                    print(f"No application found with ID {app_id}.")
                else:
                    print(f"\nApplication found: {app[1]} - {app[2]} (Current status: {app[4]})")
                    confirm = input("Update this application? (y/n): ").strip().lower()
                    if confirm == "y":
                        new_status = get_valid_status()
                        update_status(app_id, new_status)
                    else:
                        print("Update cancelled.")

            elif choice == "7":
                app_id = int(input("Enter application ID to delete: "))
                app = get_application_by_id(app_id)
                if app is None:
                    print(f"No application found with ID {app_id}.")
                else:
                    print(f"\nApplication found: {app[1]} - {app[2]}")
                    confirm = input("Are you sure you want to delete this? (y/n): ").strip().lower()
                    if confirm == "y":
                        delete_application(app_id)
                    else:
                        print("Deletion cancelled.")

            elif choice == "8":
                print("Exiting... Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1-8.")

        except ValueError:
            print("Invalid input! Please enter a valid number for ID.")

        except mysql.connector.Error as db_error:
            print(f"Database error occurred: {db_error}")

        except Exception as e:
            print(f"Something went wrong: {e}")


main_menu()