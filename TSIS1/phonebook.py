import json
import csv
from connect import connect

def export_to_json():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.first_name, c.last_name, c.email, c.birthday, g.name 
        FROM contacts c LEFT JOIN groups g ON c.group_id = g.id
    """)
    rows = cur.fetchall()
    data = [{"first_name": r[0], "last_name": r[1], "email": r[2], "birthday": str(r[3]), "group": r[4]} for r in rows]
    
    with open('contacts.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Successfully exported to contacts.json")
    cur.close()
    conn.close()

def import_from_json():
    filename = 'contacts.json'
    conn = connect()
    cur = conn.cursor()
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data:
                cur.execute("SELECT id FROM contacts WHERE first_name = %s", (item['first_name'],))
                if cur.fetchone():
                    choice = input(f"Contact '{item['first_name']}' already exists. Skip or Overwrite? (s/o): ")
                    if choice.lower() == 's': 
                        continue
                
                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, email, birthday)
                    VALUES (%s, %s, %s, %s) ON CONFLICT (first_name) DO UPDATE 
                    SET last_name = EXCLUDED.last_name, email = EXCLUDED.email, birthday = EXCLUDED.birthday
                """, (item['first_name'], item['last_name'], item['email'], item['birthday']))
        conn.commit()
        print("JSON import completed.")
    except FileNotFoundError:
        print("Error: File not found.")
    finally:
        cur.close()
        conn.close()

def search_console():
    query = input("Enter search query: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    results = cur.fetchall()
    if not results:
        print("No results found.")
    else:
        for row in results:
            print(row)
    cur.close()
    conn.close()

def import_from_csv(filename='contacts.csv'):
    conn = connect()
    if not conn: return
    cur = conn.cursor()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (row['group_name'],))
                cur.execute("SELECT id FROM groups WHERE name = %s", (row['group_name'],))
                group_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (row['first_name'], row['last_name'], row['email'], row['birthday'], group_id))
                contact_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, row['phone'], row['phone_type']))
                
        conn.commit()
        print("CSV import finished.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Search")
        print("2. Export JSON")
        print("3. Import JSON")
        print("4. Import CSV")
        print("5. Exit")
        
        choice = input("Option: ")
        if choice == '1': search_console()
        elif choice == '2': export_to_json()
        elif choice == '3': import_from_json()
        elif choice == '4': import_from_csv()
        elif choice == '5': break

if __name__ == "__main__":
    main()