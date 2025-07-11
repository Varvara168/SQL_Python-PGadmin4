import psycopg2
from datetime import date

def connect_db():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='1',
        host='localhost',
        port='5432',
    )

def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        second_name VARCHAR(50),
        email VARCHAR(100)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spendings (
        id SERIAL PRIMARY KEY,
        prise NUMERIC,
        created_at DATE,
        user_id INTEGER REFERENCES users(id)
    );
    """)

def return_id_users(cursor):
    cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1;")
    result = cursor.fetchone()
    if result and result[0] is not None:
        return int(result[0])
    else:
        return 0  # если в таблице нет ни одной записи

def add_user(cursor):
    print("🧑 Добавление нового пользователя:")
    id = return_id_users(cursor) + 1
    first_name = input("Имя: ")
    second_name = input("Фамилия: ")
    email = input("Email: ")
    cursor.execute("""
    INSERT INTO users (id, first_name, second_name, email)
    VALUES (%s, %s, %s, %s);
    """, (id, first_name, second_name, email))
    print("✅ Пользователь добавлен!")

def return_users(cursor):
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    if not rows:
        print("📭 Пользователи отсутствуют.")
    for i, row in enumerate(rows, start=1):
        try:
            print(f"{i}. {row}")
        except UnicodeDecodeError as e:
            print(f"⚠️ Ошибка при печати строки #{i}:", row)
            print("➡️ Причина:", e)

def return_id_spendings(cursor):
    cursor.execute("SELECT id FROM spendings ORDER BY id DESC LIMIT 1;")
    result = cursor.fetchone()
    if result and result[0] is not None:
        return int(result[0])
    else:
        return 0  # если в таблице нет ни одной записи

def add_spending(cursor):
    print("💰 Добавление траты:")
    try:
        id = return_id_spendings(cursor) + 1
        prise = float(input("Сумма траты: "))
        name = input("Описание траты: ")
        today = date.today()
        '''from datetime import datetime
        date_str = input("Введите дату (в формате ГГГГ-ММ-ДД): ")
        try:
            today = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("⚠️ Неверный формат даты! Используйте ГГГГ-ММ-ДД.")
            return ручной ввод даты 
        '''
        return_users(cursor)
        user_id = input('Какой вы пользователь (введите ID): ')
        cursor.execute("""
        INSERT INTO spendings (id, prise, created_at, user_id, name)
        VALUES (%s, %s, %s, %s, %s);
        """, (id, prise, today, user_id, name))
        print("✅ Трата добавлена!")
    except ValueError:
        print("⚠️ Неверный ввод!")

def view_spendings(cursor):
    print("📄 Все траты с именами пользователей:")
    cursor.execute("""
    SELECT s.id, s.prise, s.created_at, s.name, u.first_name
    FROM spendings s
    JOIN users u ON s.user_id = u.id;
    """)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"🧾 Трата #{row[0]} — {row[1]}₽ от {row[4]} Описание: {row[3]} #({row[2]})")
    else:
        print("❌ Трат нет.")


def view_spendings_by_user(cursor):
    name = input("Введите имя пользователя: ")
    
    # Найти ID всех пользователей с этим именем
    cursor.execute("SELECT id, first_name, second_name FROM users WHERE first_name = %s;", (name,))
    users = cursor.fetchall()

    if not users:
        print("❌ Пользователь с таким именем не найден.")
        return

    # Если несколько пользователей с одним именем — покажем всех
    if len(users) > 1:
        print("⚠️ Найдено несколько пользователей с таким именем:")
        for u in users:
            print(f"ID: {u[0]}, ФИО: {u[1]} {u[2]}")
        user_id = input("Введите нужный ID: ")
    else:
        user_id = users[0][0]

    # Вывод трат по user_id
    cursor.execute("""
        SELECT s.id, s.prise, s.created_at
        FROM spendings s
        WHERE s.user_id = %s;
    """, (user_id,))
    spendings = cursor.fetchall()

    if spendings:
        print(f"\n📄 Траты пользователя с ID {user_id}:")
        for row in spendings:
            print(f"🧾 Трата #{row[0]} — {row[1]}₽ ({row[2]})")
    else:
        print("❌ У этого пользователя нет трат.")

def delete_user_by_id(cursor):
    try:
        user_id = int(input("Введите ID пользователя, которого нужно удалить: "))

        # Проверим, существует ли такой пользователь
        cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        user = cursor.fetchone()

        if not user:
            print("❌ Пользователь не найден.")
            return

        print(f"👤 Найден: {user[1]} {user[2]}, email: {user[3]}")
        confirm = input("Вы уверены, что хотите удалить этого пользователя и все его траты? (y/n): ").lower()

        if confirm == "y":
            # Сначала удаляем траты пользователя (если есть)
            cursor.execute("DELETE FROM spendings WHERE user_id = %s;", (user_id,))
            # Затем удаляем пользователя
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            print("🗑️ Пользователь и его траты удалены.")
        else:
            print("❌ Удаление отменено.")

    except ValueError:
        print("⚠️ Неверный ввод ID.")

