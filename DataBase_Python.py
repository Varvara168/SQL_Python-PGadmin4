from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Создаём базу для всех моделей
Base = declarative_base()

# Описываем таблицу "пользователи"
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)   # ID — первичный ключ
    name = Column(String)                    # Имя пользователя
    age = Column(Integer)                    # Возраст

# Создаём подключение к базе данных SQLite
engine = create_engine("sqlite:///users.db")

# Создаём таблицу, если её ещё нет
Base.metadata.create_all(engine)

# Создаём сессию для работы с базой
Session = sessionmaker(bind=engine)
session = Session()

# Добавим пользователей, если база пока пустая
if not session.query(User).first():  # если таблица пустая
    user1 = User(name="Варвара", age=17)
    user2 = User(name="Лиса", age=21)
    user3 = User(name="Ева", age=18)
    
    session.add_all([user1, user2, user3])  # добавляем всех сразу
    session.commit()  # сохраняем изменения

# Вывод всех пользователей
print("\n📋 Все пользователи:")
all_users = session.query(User).all()  # получаем всех из таблицы
for user in all_users:
    print(f"🧍 {user.name}, {user.age} лет")

# Вывод пользователей старше 18
print("\n🔎 Пользователи старше 18:")
adult_users = session.query(User).filter(User.age > 18).all()
for user in adult_users:
    print(f"✅ {user.name}, {user.age} лет")

# Поиск пользователя по имени
print("\n🔍 Поиск пользователя с именем 'Лиса':")
found_user = session.query(User).filter(User.name == "Лиса").first()
if found_user:
    print(f"👁 Найдена: {found_user.name}, {found_user.age} лет")
else:
    print("❌ Не найдена")

# Обновление возраста Варвары
print("\n✏️ Обновление возраста Варвары до 18 лет:")
user_to_update = session.query(User).filter(User.name == "Варвара").first()
if user_to_update:
    user_to_update.age = 18
    session.commit()
    print("✅ Обновлено")

# Удаление пользователя по имени "Ева"
print("\n🗑 Удаление пользователя по имени 'Ева':")
user_to_delete = session.query(User).filter(User.name == "Ева").first()
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print("✅ Удалена")

# Итоговый список всех пользователей
print("\n📋 Итоговый список пользователей:")
final_users = session.query(User).all()
for user in final_users:
    print(f"👤 {user.name}, {user.age} лет")
