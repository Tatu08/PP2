import psycopg2
from psycopg2 import Error
import csv
import connect

def create_table():
    """Создаёт таблицу phonebook, если её ещё нет"""
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
            print("Таблица phonebook успешно создана (или уже существует).")
    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        connect.close_connection(conn)

def import_from_csv(filename="contacts.csv"):
    """Импорт контактов из CSV файла"""
    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur, open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Пропускаем заголовок, если он есть
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
        print(f"Данные из {filename} успешно импортированы.")
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
    except Error as e:
        print(f"Ошибка импорта: {e}")
    finally:
        connect.close_connection(conn)

def add_contact():
    """Добавление нового контакта"""
    username = input("Введите имя пользователя: ").strip()
    phone = input("Введите номер телефона: ").strip()
    
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
            print(f"Контакт '{username}' добавлен/обновлён.")
    except Error as e:
        print(f"Ошибка добавления: {e}")
    finally:
        connect.close_connection(conn)

def show_all():
    """Показать все контакты"""
    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, phone FROM phonebook ORDER BY username;")
            rows = cur.fetchall()
            if not rows:
                print("Телефонная книга пуста.")
                return
            print("\n--- Все контакты ---")
            for row in rows:
                print(f"ID: {row[0]:<3} | Имя: {row[1]:<20} | Телефон: {row[2]}")
    except Error as e:
        print(f"Ошибка: {e}")
    finally:
        connect.close_connection(conn)

def search_contact():
    """Поиск по имени или телефону"""
    query = input("Введите имя или часть номера для поиска: ").strip()
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
                print("Ничего не найдено.")
                return
            print("\n--- Результаты поиска ---")
            for row in rows:
                print(f"ID: {row[0]:<3} | Имя: {row[1]:<20} | Телефон: {row[2]}")
    except Error as e:
        print(f"Ошибка поиска: {e}")
    finally:
        connect.close_connection(conn)

def update_contact():
    """Обновление имени или телефона"""
    username = input("Введите текущее имя пользователя для обновления: ").strip()
    print("Что обновить?")
    print("1. Имя")
    print("2. Телефон")
    choice = input("Выберите (1/2): ")
    
    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            if choice == "1":
                new_username = input("Новое имя: ").strip()
                cur.execute("""
                    UPDATE phonebook SET username = %s 
                    WHERE username = %s;
                """, (new_username, username))
            elif choice == "2":
                new_phone = input("Новый телефон: ").strip()
                cur.execute("""
                    UPDATE phonebook SET phone = %s 
                    WHERE username = %s;
                """, (new_phone, username))
            else:
                print("Неверный выбор.")
                return
            conn.commit()
            print("Контакт обновлён.")
    except Error as e:
        print(f"Ошибка обновления: {e}")
    finally:
        connect.close_connection(conn)

def delete_contact():
    """Удаление контакта"""
    print("Удалить по:")
    print("1. Имени пользователя")
    print("2. Номеру телефона")
    choice = input("Выберите (1/2): ")
    
    conn = connect.get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            if choice == "1":
                username = input("Имя пользователя: ").strip()
                cur.execute("DELETE FROM phonebook WHERE username = %s;", (username,))
            elif choice == "2":
                phone = input("Номер телефона: ").strip()
                cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))
            else:
                print("Неверный выбор.")
                return
            conn.commit()
            print("Контакт удалён (если существовал).")
    except Error as e:
        print(f"Ошибка удаления: {e}")
    finally:
        connect.close_connection(conn)

def main_menu():
    create_table()  # Создаём таблицу при запуске
    
    while True:
        print("\n" + "="*40)
        print("     PHONEBOOK - Телефонная книга")
        print("="*40)
        print("1. Показать все контакты")
        print("2. Добавить контакт")
        print("3. Поиск контакта")
        print("4. Обновить контакт")
        print("5. Удалить контакт")
        print("6. Импорт из contacts.csv")
        print("0. Выход")
        print("="*40)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            show_all()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            import_from_csv()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main_menu()