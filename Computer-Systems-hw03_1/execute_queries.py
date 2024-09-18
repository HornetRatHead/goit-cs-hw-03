import psycopg2

#1. Отримати всі користувачі
def get_all_users(cur, conn):
    cur.execute("SELECT * FROM users;")
    return cur.fetchall()

#2. Отримати всі статуси
def get_all_statuses(cur, conn):
    cur.execute("SELECT * FROM status;")
    return cur.fetchall()

#3. Отримати всі завдання
def get_all_tasks(cur, conn):
    try:
        cur.execute("SELECT * FROM tasks;")
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error retrieving all tasks: {e}")
        return None
    cur.execute("SELECT * FROM tasks;")
    return cur.fetchall()

#4. Отримати завдання за ID користувача
def get_tasks_by_user(cur, conn, user_id):
    cur.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
    return cur.fetchall()

#5. Отримати завдання за ID статусу
def get_tasks_by_status(cur, conn, status_id):
    cur.execute("SELECT * FROM tasks WHERE status_id = %s;", (status_id,))
    return cur.fetchall()
 
#6. Оновити статус завдання 
def update_task_status(cur, conn, task_id, new_status_id):
    cur.execute("UPDATE tasks SET status_id = %s WHERE id = %s;", (new_status_id, task_id))
    conn.commit()

#7. Отримати користувачів, які не виконували завдання
def get_users_with_no_tasks(cur, conn):
    cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);")
    return cur.fetchall()

#8. Додати нове завдання
def add_task(cur, conn, user_id, task_description, status): 
    cur.execute("INSERT INTO tasks (user_id, description, status) VALUES (%s, %s, %s);", 
                (user_id, task_description, status))
    conn.commit()

#9. Видалити завдання
def get_tasks_not_completed(cur, conn):
    cur.execute("SELECT tasks.* FROM tasks JOIN status ON tasks.status_id = status.id WHERE status.name != 'completed';")
    return cur.fetchall()

#10. Видалити завдання
def delete_task(cur, conn, task_id):
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()

#11. Пошук користувачів за email
def find_users_by_email(cur, conn, email_pattern):
    pattern = f"%{email_pattern}%"
    cur.execute("SELECT * FROM users WHERE email LIKE %s;", (pattern,))
    return cur.fetchall()

#12. Оновити ім'я користувача
def update_user_name(cur, conn, user_id, new_name):
    cur.execute("UPDATE users SET fullname = %s WHERE id = %s;", (new_name, user_id))
    conn.commit()

#13. Отримати кількість завдань по кожному статусу    
def get_task_counts_by_status(cur, conn):
    cur.execute("SELECT status.name, COUNT(*) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY status.name;")
    return cur.fetchall()

#14. Отримати список користувачів без завдань
def get_tasks_for_users_with_email_domain(cur, conn, domain):
    cur.execute("SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s;", (f'%@{domain}%',))
    return cur.fetchall()

#15. Отримати список користувачів без описаного завдання
def get_tasks_without_description(cur, conn):
    cur.execute("SELECT * FROM tasks WHERE description IS NULL;")
    return cur.fetchall()

#16. Отримати користувачів, які виконували завдання
def get_users_and_tasks_in_progress(cur, conn):
    cur.execute("SELECT users.*, tasks.* FROM users INNER JOIN tasks ON users.id = tasks.user_id INNER JOIN status ON tasks.status_id = status.id WHERE status.name = 'in progress';")
    return cur.fetchall()

#17. Отримати користувачів, які виконували завдання
def get_users_and_task_counts(cur, conn):
    cur.execute("SELECT users.*, COUNT(tasks.id) FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.id;")
    return cur.fetchall()

def menu(cur, conn):
    while True:
        print("\nМеню:")
        print("1. Отримати всі користувачі")
        print("2. Отримати всі статуси")
        print("3. Отримати всі завдання")
        print("4. Отримати завдання за певним користувачем")
        print("5. Отримати завдання за певним статусом іd (1 = new, 2 =in progress, 3 = completed)")
        print("6. Оновити статус завдання")
        print("7. Отримати список користувачів без завдань")
        print("8. Додати нове завдання")
        print("9. Отримати всі завдання, що не завершені")
        print("10. Видалити завдання")
        print("11. Знайти користувачів за електронною поштою")
        print("12. Оновити ім'я користувача")
        print("13. Отримати кількість завдань за кожним статусом")
        print("14. Отримати завдання для користувачів з певною доменною частиною електронної пошти")
        print("15. Отримати завдання без опису")
        print("16. Отримати користувачів та їхні завдання у статусі 'in progress'")
        print("17. Отримати користувачів та кількість їхніх завдань")
        print("18. Вихід")

        choice = input("Оберіть команду (1-18): ")

        if choice == "1":
            print(get_all_users(cur, conn))
        elif choice == "2":
            print(get_all_statuses(cur, conn))
        elif choice == "3":
            print(get_all_tasks(cur, conn))
        elif choice == "4":
            user_id = int(input("Введіть user_id: "))
            print(get_tasks_by_user(cur, conn, user_id))
        elif choice == "5":
            status = input("Введіть статус: ")
            print(get_tasks_by_status(cur, conn, status))
        elif choice == "6":
            task_id = int(input("Введіть id завдання: "))
            new_status = input("Введіть новий статус: ")
            update_task_status(cur, conn, task_id, new_status)
        elif choice == "7":
            print(get_users_with_no_tasks(cur, conn))
        elif choice == "8":
            user_id = int(input("Введіть user_id: "))
            task_description = input("Введіть опис завдання: ")
            status = input("Введіть статус: ")
            add_task(cur, conn, user_id, task_description, status)
        elif choice == "9":
            print(get_tasks_not_completed(cur, conn))
        elif choice == "10":
            task_id = int(input("Введіть id завдання: "))
            delete_task(cur, conn, task_id)
        elif choice == "11":
            email_pattern = input("Введіть шаблон електронної пошти: ")
            print(find_users_by_email(cur, conn, email_pattern))
        elif choice == "12":
            user_id = int(input("Введіть user_id: "))
            new_name = input("Введіть нове ім'я: ")
            update_user_name(cur, conn, user_id, new_name)
        elif choice == "13":
            print(get_task_counts_by_status(cur, conn))
        elif choice == "14":
            domain = input("Введіть домен електронної пошти: ")
            print(get_tasks_for_users_with_email_domain(cur, conn, domain))
        elif choice == "15":
            print(get_tasks_without_description(cur, conn))
        elif choice == "16":
            print(get_users_and_tasks_in_progress(cur, conn))
        elif choice == "17":
            print(get_users_and_task_counts(cur, conn))
        elif choice == "18":
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    menu(cur, conn) 
