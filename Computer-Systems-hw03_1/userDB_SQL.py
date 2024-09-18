#userDB_SQL

import subprocess
import psycopg2
from psycopg2 import sql
from faker import Faker
import random
import time


# Створюэмо контейнер
def create_postgres_container(container_name, db_user, db_password, db_name, port):
    try:
        # Формуємо команду для запуску PostgreSQL контейнера
        docker_command = [
            "docker", "run", "--name", container_name,
            "-e", f"POSTGRES_USER={db_user}",
            "-e", f"POSTGRES_PASSWORD={db_password}",
            "-e", f"POSTGRES_DB={db_name}",
            "-p", f"{port}:5432",
            "-d", "postgres"
        ]

        # Виконуємо команду
        subprocess.run(docker_command, check=True)
        print(f"Контейнер PostgreSQL з ім'ям '{container_name}' запущено на порту {port}.")

    except subprocess.CalledProcessError as e:
        print(f"Помилка при створенні контейнера: {e}")

    
# Прибираемо контейнер
def stop_and_remove_container(container_name):
    try:
        # Остановка і видалення контейнера
        subprocess.run(["docker", "stop", container_name], check=True)
        subprocess.run(["docker", "rm", container_name], check=True)
        print(f"Контейнер '{container_name}' було зупинено та видалено.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при видаленні контейнера: {e}")

# Змінні для глобального доступу
conn = None
cur = None

# Утворюэмо з'єднання з PostgreSQL
def db_connection():
    
    global conn, cur

    try:
        conn = psycopg2.connect(
            host = "localhost",
            database = db_name,
            user = db_user,
            password = db_password
        )
        cur = conn.cursor()
        print("З'єднання з PostgreSQL встановлено!")
    except psycopg2.OperationalError as e:
        print(f"Помилка з'єднання: {e}")


fake = Faker()

# Функція для створення таблиці users
def create_users_table():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    ''')
    conn.commit()

# Функція для створення таблиці status
def create_status_table():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
    ''')
    conn.commit()

# Функція для створення таблиці tasks
def create_tasks_table():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER REFERENCES status(id) ON DELETE SET NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()

# Функція для вставки даних в таблицю status
def insert_status():
    statuses = [('new',), ('in progress',), ('completed',)]
    query = "INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING"
    cur.executemany(query, statuses)
    conn.commit()

# Функція для вставки випадкових користувачів
def seed_users(n):
    for _ in range(n):
        fullname = fake.name()
        email = fake.unique.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
    conn.commit()

# Функція для вставки випадкових завдань
def seed_tasks(n):
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]
    
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        description = fake.text()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )
    conn.commit()

# Основна функція для створення всіх таблиць та наповнення їх даними
def tabs_creations():
    # Створення таблиць
    create_users_table()
    create_status_table()
    create_tasks_table()
    
    # Вставка статусів
    insert_status()
    
    # Вставка користувачів та завдань
    seed_users(10)  # Вставка 10 випадкових користувачів
    seed_tasks(20)  # Вставка 20 випадкових завдань


# Друк наявних таблиц у консолью Перевіряємо наявність та заповнення
def print_users():
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    print("\n--- Users Table ---")
    for row in rows:
        print(row)

def print_status():
    cur.execute("SELECT * FROM status")
    rows = cur.fetchall()
    print("\n--- Status Table ---")
    for row in rows:
        print(row)

def print_tasks():
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    print("\n--- Tasks Table ---")
    for row in rows:
        print(row)


if __name__ == "__main__":

    container_name = "temporary_PostgreSQL"
    db_user = "current_user"
    db_password = "1111"
    db_name = "zeroDB"
    port = 5432  # порт для підключення

    stop_and_remove_container(container_name) # спочатку видаляэмо, щоб уникнути помилок

    create_postgres_container(container_name, db_user, db_password, db_name, port)

    time.sleep(10)

    db_connection()
   
    print_users()
    print_status()
    print_tasks()

    # Закриття з'єднання
    cur.close()
    conn.close()

    # stop_and_remove_container(container_name) # прибираэмо за собою