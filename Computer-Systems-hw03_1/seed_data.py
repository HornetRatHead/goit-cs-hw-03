import psycopg2
from faker import Faker
import random

fake = Faker()

# Параметри підключення
db_name = 'zeroDB'
db_user = 'current_user'
db_password = '1111'

conn = None
cur = None

# Утворюємо з'єднання з PostgreSQL
def db_connection():
    global conn, cur

    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname=db_name,   # Параметр dbname
            user=db_user,     # Параметр user
            password=db_password,  # Параметр password
            port=5432         # Параметр port (за замовчуванням 5432)
        )
        cur = conn.cursor()
        print("З'єднання з PostgreSQL встановлено!")
    except psycopg2.OperationalError as e:
        print(f"Помилка з'єднання: {e}")

# Функція для створення таблиці users
def create_users_table(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    ''')
    conn.commit()

# Функція для створення таблиці status
def create_status_table(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
    ''')
    conn.commit()

# Функція для створення таблиці tasks
def create_tasks_table(cur, conn):
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

# Вставка статусів
def insert_status(cur, conn):
    statuses = [('new',), ('in progress',), ('completed',)]
    query = "INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING"
    cur.executemany(query, statuses)
    conn.commit()

# Вставка випадкових користувачів
def seed_users(cur, conn, n):
    for _ in range(n):
        fullname = fake.name()
        email = fake.unique.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
    conn.commit()

# Вставка випадкових завдань
def seed_tasks(cur, conn, n):
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

def get_all_users(cur, conn):
    cur.execute("SELECT * FROM users;")
    return cur.fetchall()

# Основна функція для створення всіх таблиць та наповнення їх даними
def tabs_creations(cur, conn):
   
        # Створення таблиць
        create_users_table(cur, conn)
        print("Таблиця users успішно створені!")
        create_status_table(cur, conn)
        print("Таблиця status успішно створені!")
        create_tasks_table(cur, conn)
        print("Таблиця tasks успішно створені!")                                                                                                                                                                                                  
        
        # Вставка статусів
        insert_status(cur, conn)
        print("Статуси успішно вставлені!")

        # Вставка користувачів та завдань
        seed_users(cur, conn, 10)  # Вставка 10 випадкових користувачів
        print("Користувачі успішно вставлені!")
        seed_tasks(cur, conn, 20)  # Вставка 20 випадкових завдань
        print("Завдання успішно вставлені!")

        print(get_all_users(cur, conn))


if __name__ == "__main__":
    db_connection()
    tabs_creations(cur, conn)
