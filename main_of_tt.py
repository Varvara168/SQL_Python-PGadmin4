from tt import *

def main():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        create_tables(cursor)
        conn.commit()

        while True:
            print('-----------------------------')
            print("\n📌 Выбери действие:")
            print("1 — Добавить пользователя")
            print("2 — Добавить трату")
            print("3 — Посмотреть все траты")
            print("4 — Вывести всех пользователей")
            print('5 - Траты по имени')
            print('6 - Удаление пользователя')
            print("0 — Выход")

            choice = input("👉 Ввод: ")
            print('-----------------------------')

            if choice == "1":
                add_user(cursor)
            elif choice == "2":
                add_spending(cursor)
            elif choice == "3":
                view_spendings(cursor)
            elif choice == "4":
                return_users(cursor)
            elif choice == "5":
                view_spendings_by_user(cursor)
            elif choice == "6":
                delete_user_by_id(cursor)
            elif choice == "0":
                print("👋 Пока!")
                break
            else:
                print("❌ Неверный выбор!")

            conn.commit()

    except Exception as e:
        print("❌ Ошибка:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

main()