#main.py

import os
import subprocess
import sys
from pymongo import MongoClient, errors
from MongoDB_Docker import mongodb_deploy

def check_and_setup_venv():
    """
    Перевіряє наявність віртуального середовища та створює його, якщо відсутнє.
    """
    venv_path = os.path.join(os.getcwd(), 'venv')
    
    # Якщо віртуальне середовище не існує, створюємо нове
    if not os.path.exists(venv_path):
        print("Віртуальне середовище не знайдено, створюється нове...")
        subprocess.run(['setup.bat'], shell=True)
    
    # Перевірка, чи активоване віртуальне середовище
    if sys.prefix != venv_path:
        print(f"Увага! Віртуальне середовище не активоване: {venv_path}. Продовження виконання.")

def connect_to_mongodb():
    """
    Підключається до MongoDB та повертає колекцію 'cats' бази даних 'cats_db'.
    """
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["cats_db"]  # Створюємо або підключаємося до бази даних
        collection = db["cats"]  # Створюємо або підключаємося до колекції
        print("Успішно підключено до MongoDB.")
        return collection
    except errors.ConnectionError as e:
        print(f"Помилка підключення до MongoDB: {e}")
        sys.exit(1)  # Вихід зі скрипту при неможливості підключення

# 1. Create (Створення)
def add_cat(name, age, features, collection):
    """Додає кота до бази даних."""
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        print(f"Кота додано з _id: {result.inserted_id}")
    except errors.PyMongoError as e:
        print(f"Помилка при додаванні кота: {e}")

# 2. Read (Читання)
def get_all_cats(collection):
    """Виводить всіх котів із бази даних."""
    try:
        # Підрахунок кількості документів у колекції
        count = collection.count_documents({})
        if count == 0:
            print("Записів немає.")
        else:
            cats = collection.find()
            for cat in cats:
                print(cat)
    except errors.PyMongoError as e:
        print(f"Помилка при читанні даних: {e}")

def get_cat_by_name(name, collection):
    """Шукає кота за ім'ям та виводить інформацію про нього."""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка при пошуку кота: {e}")

# 3. Update (Оновлення)
def update_cat_age_by_name(name, new_age, collection):
    """Оновлює вік кота за його ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Вік кота {name} оновлено до {new_age}.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка при оновленні віку кота: {e}")

def add_feature_to_cat(name, new_feature, collection):
    """Додає нову характеристику до списку кота."""
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count > 0:
            print(f"Характеристику '{new_feature}' додано коту {name}.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка при додаванні характеристики коту: {e}")

# 4. Delete (Видалення)
def delete_cat_by_name(name, collection):
    """Видаляє кота з бази за ім'ям."""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кота з ім'ям {name} видалено.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")

def delete_all_cats(collection):
    """Видаляє всі записи про котів із бази даних."""
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів.")
    except errors.PyMongoError as e:
        print(f"Помилка при видаленні всіх записів: {e}")

# Меню для взаємодії з користувачем
def main(collection):
    while True:
        print("\n--- Меню ---")
        print("1. Додати кота")
        print("2. Показати всіх котів")
        print("3. Знайти кота за ім'ям")
        print("4. Оновити вік кота за ім'ям")
        print("5. Додати характеристику коту")
        print("6. Видалити кота за ім'ям")
        print("7. Видалити всіх котів")
        print("8. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            name = input("Ім'я кота: ")
            age = int(input("Вік кота: "))
            features = input("Характеристики кота (через кому): ").split(",")
            add_cat(name, age, [feature.strip() for feature in features], collection)

        elif choice == "2":
            get_all_cats(collection)

        elif choice == "3":
            name = input("Введіть ім'я кота: ")
            get_cat_by_name(name, collection)

        elif choice == "4":
            name = input("Введіть ім'я кота: ")
            new_age = int(input("Введіть новий вік кота: "))
            update_cat_age_by_name(name, new_age, collection)

        elif choice == "5":
            name = input("Введіть ім'я кота: ")
            new_feature = input("Введіть нову характеристику: ")
            add_feature_to_cat(name, new_feature, collection)

        elif choice == "6":
            name = input("Введіть ім'я кота, якого бажаєте видалити: ")
            delete_cat_by_name(name, collection)

        elif choice == "7":
            confirmation = input("Ви впевнені, що хочете видалити всіх котів? (y/n): ")
            if confirmation.lower() == 'y':
                delete_all_cats(collection)

        elif choice == "8":
            break

        else:
            print("Невірний вибір, спробуйте ще раз.")

if __name__ == "__main__":
    # Деплой БД
    mongodb_deploy()

    # Перевірка та створення віртуального середовища
    check_and_setup_venv()

    # Підключення до MongoDB
    collection = connect_to_mongodb()

    # Запуск основної програми з колекцією
    main(collection)