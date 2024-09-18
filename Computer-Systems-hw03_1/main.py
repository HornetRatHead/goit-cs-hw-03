#userDB_SQL

import subprocess
import psycopg2
from psycopg2 import sql
from faker import Faker
import random
import time
from execute_queries import menu
from seed_data import tabs_creations

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

# Утворюємо з'єднання з PostgreSQL
def db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname=db_name,   
            user=db_user,     
            password=db_password,  
            port=5432         
        )
        cur = conn.cursor()
        print("З'єднання з PostgreSQL встановлено!")
        return conn, cur
    except psycopg2.OperationalError as e:
        print(f"Помилка з'єднання: {e}")
        return None, None


if __name__ == "__main__":

    container_name = "temporary_PostgreSQL"
    db_user = "current_user"
    db_password = "1111"
    db_name = "zeroDB"
    port = 5432  # порт для підключення

    stop_and_remove_container(container_name) # спочатку видаляэмо, щоб уникнути помилок

    create_postgres_container(container_name, db_user, db_password, db_name, port)

    print("Чекаэмо поки підніметься база")
    time.sleep(5)

    conn, cur = db_connection()

    if cur and conn:  # Перевірка чи з'єднання було успішним
        tabs_creations(cur, conn)

        menu(cur, conn)

    else:
        print("З'єднання з базою даних не вдалося.")

    # Закриття з'єднання
    cur.close()
    conn.close()

    