import psycopg2

# Утворюємо з'єднання з PostgreSQL
def db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="zeroDB",
            user="current_user",
            password="1111"
        )
        cur = conn.cursor()
        print("З'єднання з PostgreSQL встановлено!")
        return conn, cur
    except psycopg2.OperationalError as e:
        print(f"Помилка з'єднання: {e}")

# Створення таблиці users
def create_users_table(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    ''')
    conn.commit()

# Створення таблиці status
def create_status_table(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
    ''')
    conn.commit()

# Створення таблиці tasks
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

if __name__ == "__main__":
    conn, cur = db_connection()

    # Створення таблиць
    create_users_table(cur, conn)
    create_status_table(cur, conn)
    create_tasks_table(cur, conn)

    # Закриття з'єднання
    cur.close()
    conn.close()
