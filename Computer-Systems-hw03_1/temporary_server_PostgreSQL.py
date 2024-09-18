#temporary_server_PostgreSQL

import subprocess

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

def stop_and_remove_container(container_name):
    try:
        # Остановка і видалення контейнера
        subprocess.run(["docker", "stop", container_name], check=True)
        subprocess.run(["docker", "rm", container_name], check=True)
        print(f"Контейнер '{container_name}' було зупинено та видалено.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при видаленні контейнера: {e}")

if __name__ == "__main__":
    # Параметри контейнера PostgreSQL
    container_name = "temporary_PostgreSQL"
    db_user = "current_user"
    db_password = "1111"
    db_name = "zeroDB"
    port = 5432  # порт для підключення

    # Зупинка і видалення контейнера 
    stop_and_remove_container(container_name)

    # Створення контейнера
    create_postgres_container(container_name, db_user, db_password, db_name, port)

   
