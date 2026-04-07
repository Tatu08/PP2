import psycopg2
from psycopg2 import Error
import csv
import connect
import sys

sys.stdout.reconfigure(encoding='utf-8')


def create_table():
    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(20) NOT NULL
                );
            """)
            conn.commit()
            print("Table phonebook successfully created (or already exists).")
    except Error as e:
        print(f"Error during table creation: {e}")
    finally:
        connect.close_connection(conn)


def import_from_csv(filename="contacts.csv"):
    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur, open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) >= 2:
                    username = row[0].strip()
                    phone = row[1].strip()

                    cur.execute("""
                        INSERT INTO phonebook (username, phone)
                        VALUES (%s, %s)
                        ON CONFLICT (username) DO NOTHING;
                    """, (username, phone))

        conn.commit()
        print(f"Data from {filename} successfully imported.")
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except Error as e:
        print(f"Import error: {e}")
    finally:
        connect.close_connection(conn)


def add_contact():
    username = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO phonebook (username, phone)
                VALUES (%s, %s)
                ON CONFLICT (username)
                DO UPDATE SET phone = EXCLUDED.phone;
            """, (username, phone))

            conn.commit()
            print("Contact added/updated.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connect.close_connection(conn)


def show_all():
    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, phone FROM phonebook ORDER BY id;")
            rows = cur.fetchall()

            if not rows:
                print("Phonebook is empty.")
                return

            print("\n--- All contacts (Sorted by ID) ---")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        connect.close_connection(conn)


def search_contact():
    query = input("Enter name or number: ").strip()

    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, phone
                FROM phonebook
                WHERE username ILIKE %s OR phone ILIKE %s;
            """, (f"%{query}%", f"%{query}%"))

            rows = cur.fetchall()

            if not rows:
                print("Nothing found.")
                return

            print("\n--- Results ---")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

    except Error as e:
        print(f"Search error: {e}")
    finally:
        connect.close_connection(conn)


def update_contact():
    username = input("Enter name: ").strip()

    print("1. Name")
    print("2. Phone")
    choice = input("Choose: ")

    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            if choice == "1":
                new_username = input("New name: ").strip()
                cur.execute(
                    "UPDATE phonebook SET username=%s WHERE username=%s;",
                    (new_username, username)
                )
            elif choice == "2":
                new_phone = input("New phone: ").strip()
                cur.execute(
                    "UPDATE phonebook SET phone=%s WHERE username=%s;",
                    (new_phone, username)
                )
            else:
                print("Choice error")
                return

            conn.commit()
            print("Updated!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        connect.close_connection(conn)


def delete_contact():
    username = input("Enter name: ").strip()

    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE username=%s;", (username,))
            conn.commit()
            print("Deleted!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        connect.close_connection(conn)


def show_paged():
    limit = int(input("How many contacts per page? (Limit): "))
    offset = int(input("How many contacts to skip? (Offset): "))

    conn = connect.get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paged(%s, %s);", (limit, offset))
            rows = cur.fetchall()
            
            print(f"\n--- Paged Results (Limit: {limit}, Offset: {offset}) ---")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connect.close_connection(conn)

def delete_by_proc():
    search_val = input("Enter name or phone to delete: ").strip()

    conn = connect.get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact_proc(%s);", (search_val,))
            conn.commit()
            print(f"Record matching '{search_val}' has been deleted.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connect.close_connection(conn)

def main_menu():
    create_table()
    while True:
        print("\n====== PHONEBOOK (SQL Functions/Procedures) ======")
        print("1. Show all")
        print("2. Add contact")
        print("3. Search")
        print("4. Update")
        print("5. Delete (Basic SQL)")
        print("6. Show Paged (SQL Function)")      
        print("7. Delete Advanced (SQL Procedure)")   
        print("8. Import CSV")
        print("0. Exit")

        choice = input("Choose: ")
        if choice == "1": show_all()
        elif choice == "2": add_contact()
        elif choice == "3": search_contact()
        elif choice == "4": update_contact()
        elif choice == "5": delete_contact()
        elif choice == "6": show_paged()
        elif choice == "7": delete_by_proc()
        elif choice == "8": import_from_csv()
        elif choice == "0": break
        
if __name__ == "__main__":
    main_menu()