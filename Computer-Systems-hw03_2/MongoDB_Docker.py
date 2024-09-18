import subprocess
import sys
import os
from pymongo import MongoClient, errors

def check_docker_status():
    try:
        # Перевірка доступності Docker Daemon
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Docker Daemon не запущено. Переконайтеся, що Docker працює.")
            print("Помилка:", result.stderr)
            sys.exit(1)
    except FileNotFoundError:
        print("Docker CLI не знайдено. Переконайтеся, що Docker встановлено та додано до PATH.")
        sys.exit(1)

def start_mongodb_container():
    try:
        # Створюємо та запускаємо контейнер MongoDB
        subprocess.run([
            'docker', 'run', '--name', 'mongodb_container', '-p', '27017:27017', '-d', 'mongo'
        ], check=True)
        print("Контейнер MongoDB створено та запущено.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при запуску контейнера: {e}")
        sys.exit(1)

def mongodb_deploy():
    check_docker_status()
    start_mongodb_container()


if __name__ == "__main__":
    mongodb_deploy()
    