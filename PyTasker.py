import json
import os
import csv
import shutil
from datetime import datetime, date, timedelta

FILE = "tasks.json"
HISTORY_FILE = "task_history.json"
BACKUP_FILE = "tasks_backup.json"

# FILE HANDLING

def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

def save_history():
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

def add_history(action):
    history.append({
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "action": action
    })
    save_history()

# UTILITY FUNCTIONS

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPress Enter to continue...")

def get_due_date():
    while True:
        value = input("Enter Due Date (DD-MM-YYYY): ")

        try:
            datetime.strptime(value, "%d-%m-%Y")
            return value
        except ValueError:
            print("Invalid date! Please use DD-MM-YYYY.")

def get_export_date(message):
    while True:
        value = input(message)

        try:
            return datetime.strptime(
                value,
                "%d-%m-%Y"
            ).date()
        except ValueError:
            print("Invalid date! Please use DD-MM-YYYY.")

def get_task_number():
    try:
        return int(input("Enter Task Number: "))
    except ValueError:
        print("Please enter a valid number.")
        return -1

# ADD TASK

def add_task():
    print("\nADD TASK")
    task = input("Task Name: ")
    description = input("Description: ")

    priority = input("Priority (High/Medium/Low): ").capitalize()

    while priority not in ["High", "Medium", "Low"]:
        print("Invalid priority.")

        priority = input("Priority (High/Medium/Low): ").capitalize()

    category = input("Category: ").capitalize()

    tags = input("Tags (example: python,study,project): ")

    due_date = get_due_date()
    created_date = date.today().strftime("%d-%m-%Y")

    task_id = "T" + str(len(tasks) + 1).zfill(3)

    new_task = {
        "id": task_id,
        "task": task,
        "description": description,
        "priority": priority,
        "category": category,
        "tags": tags,
        "created_date": created_date,
        "due_date": due_date,
        "done": False
    }

    tasks.append(new_task)
    save_tasks()

    add_history(
        f"Added task: {task}"
    )

    print("\nTask Added Successfully! ✅")
    pause()

# DISPLAY TASK

def display_task(number, task):
    status = "✓" if task["done"] else " "

    print(f"\n{number}. [{status}] {task['task']}")
    print(f"   ID          : {task['id']}")
    print(f"   Description : {task['description']}")
    print(f"   Priority    : {task['priority']}")
    print(f"   Category    : {task['category']}")
    print(f"   Tags        : {task['tags']}")
    print(f"   Created     : {task['created_date']}")
    print(f"   Due Date    : {task['due_date']}")

# VIEW TASKS

def view_tasks():
    if not tasks:
        print("\nNo tasks found.")
        pause()
        return

    today = date.today()
    tomorrow = today + timedelta(days=1)

    overdue = []
    today_tasks = []
    tomorrow_tasks = []
    upcoming = []
    completed = []

    for i, task in enumerate(tasks, 1):
        due = datetime.strptime(task["due_date"],"%d-%m-%Y").date()

        if task["done"]:
            completed.append((i, task))

        elif due < today:
            overdue.append((i, task))

        elif due == today:
            today_tasks.append((i, task))

        elif due == tomorrow:
            tomorrow_tasks.append((i, task))

        else:
            upcoming.append((i, task))

    print("\n📋 TASK LIST")
    print("------------------------------")

    display_group("⚠️ OVERDUE",overdue)

    display_group("📅 TODAY",today_tasks)

    display_group("🌅 TOMORROW",tomorrow_tasks)

    display_group("📆 UPCOMING",upcoming)

    display_group("✅ COMPLETED",completed)

    pause()


def display_group(title, task_list):
    print(f"\n{title}")
    print("------------------------------")

    if not task_list:
        print("No tasks.")

    for number, task in task_list:
        display_task(number, task)

# EDIT TASK

def edit_task():
    if not tasks:
        print("\nNo tasks found.")
        pause()
        return

    show_simple_tasks()

    number = get_task_number()

    if number < 1 or number > len(tasks):
        print("Invalid Task Number.")
        pause()
        return

    task = tasks[number - 1]

    print("\nEDIT TASK")
    print(f"Current Task: {task['task']}")

    new_task = input("New Task (press Enter to keep current): ")

    if new_task:
        task["task"] = new_task

    new_description = input( "New Description (Enter to keep current): ")

    if new_description:
        task["description"] = new_description

    new_priority = input("New Priority (High/Medium/Low): ").capitalize()

    if new_priority in ["High", "Medium", "Low"]:
        task["priority"] = new_priority

    new_category = input("New Category (Enter to keep current): ")

    if new_category:
        task["category"] = new_category.capitalize()

    new_tags = input("New Tags (Enter to keep current): ")

    if new_tags:
        task["tags"] = new_tags

    change_date = input("Change Due Date? (y/n): ").lower()

    if change_date == "y":
        task["due_date"] = get_due_date()

    save_tasks()

    add_history(f"Edited task: {task['task']}")

    print("\nTask Updated Successfully! ✏️")
    pause()

# COMPLETE TASK

def complete_task():
    if not tasks:
        print("\nNo tasks found.")
        pause()
        return

    show_simple_tasks()

    number = get_task_number()

    if 1 <= number <= len(tasks):
        tasks[number - 1]["done"] = True
        save_tasks()
        add_history(f"Completed task: {tasks[number - 1]['task']}")

        print("\nTask Completed! ✅")
    else:
        print("\nInvalid Task Number.")

    pause()

# MARK PENDING

def mark_pending():
    if not tasks:
        print("\nNo tasks found.")
        pause()
        return

    show_simple_tasks()

    number = get_task_number()

    if 1 <= number <= len(tasks):
        tasks[number - 1]["done"] = False
        save_tasks()

        add_history(f"Marked pending: {tasks[number - 1]['task']}")

        print("\nTask Marked as Pending! 🔄")
    else:
        print("\nInvalid Task Number.")

    pause()

# DELETE TASK

def delete_task():
    if not tasks:
        print("\nNo tasks found.")
        pause()
        return

    show_simple_tasks()

    number = get_task_number()

    if 1 <= number <= len(tasks):
        deleted = tasks.pop(number - 1)

        save_tasks()

        add_history(f"Deleted task: {deleted['task']}")

        print(f"\n'{deleted['task']}' deleted successfully! 🗑️")
    else:
        print("\nInvalid Task Number.")

    pause()

# SEARCH TASK

def search_task():
    if not tasks:
        print("\nNo tasks found.")
        pause()
        return

    keyword = input("\nEnter keyword: ").lower()

    found = False

    print("\n🔎 SEARCH RESULTS")
    print("------------------------------")

    for i, task in enumerate(tasks, 1):
        searchable = (
            task["task"] + " " +
            task["description"] + " " +
            task["category"] + " " +
            task["tags"]
        ).lower()

        if keyword in searchable:
            display_task(i, task)
            found = True

    if not found:
        print("No matching tasks found.")

    pause()

# FILTER TASKS

def filter_tasks():
    if not tasks:
        print("\nNo tasks found.")
        pause()
        return

    print("\n🔍 FILTER TASKS")
    print("------------------------------")
    print("1. Pending")
    print("2. Completed")
    print("3. High Priority")
    print("4. Medium Priority")
    print("5. Low Priority")
    print("6. Today")
    print("7. Tomorrow")
    print("8. Overdue")
    print("9. Category")

    choice = input("Choose filter: ")

    result = []
    today = date.today()

    for i, task in enumerate(tasks, 1):
        due = datetime.strptime(task["due_date"],"%d-%m-%Y").date()

        if choice == "1" and not task["done"]:
            result.append((i, task))

        elif choice == "2" and task["done"]:
            result.append((i, task))

        elif choice == "3" and task["priority"] == "High":
            result.append((i, task))

        elif choice == "4" and task["priority"] == "Medium":
            result.append((i, task))

        elif choice == "5" and task["priority"] == "Low":
            result.append((i, task))

        elif choice == "6" and due == today:
            result.append((i, task))

        elif choice == "7" and due == today + timedelta(days=1):
            result.append((i, task))

        elif choice == "8" and due < today and not task["done"]:
            result.append((i, task))

    if choice == "9":
        category = input("Enter category: ").lower()

        for i, task in enumerate(tasks, 1):
            if task["category"].lower() == category:
                result.append((i, task))

    print("\n🔍 FILTER RESULTS")
    print("------------------------------")

    if not result:
        print("No tasks found.")
    else:
        for i, task in result:
            display_task(i, task)

    pause()

# SIMPLE TASK VIEW

def show_simple_tasks():
    print("\nTASKS")
    print("------------------------------")

    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else " "

        print(
            f"{i}. [{status}] "
            f"{task['task']} | "
            f"{task['priority']} | "
            f"{task['due_date']}"
        )

# DASHBOARD

def dashboard():
    total = len(tasks)

    if total == 0:
        print("\nNo tasks available.")
        pause()
        return

    completed = sum(task["done"] for task in tasks)

    pending = total - completed
    today = date.today()

    overdue = 0
    today_count = 0
    high_priority = 0

    for task in tasks:
        due = datetime.strptime(task["due_date"],"%d-%m-%Y").date()

        if not task["done"] and due < today:
            overdue += 1

        if not task["done"] and due == today:
            today_count += 1

        if task["priority"] == "High":
            high_priority += 1

    percentage = (completed / total) * 100

    print("\n📊 DASHBOARD")
    print("------------------------------")
    print(f"Total Tasks       : {total}")
    print(f"Completed         : {completed}")
    print(f"Pending           : {pending}")
    print(f"Due Today         : {today_count}")
    print(f"Overdue           : {overdue}")
    print(f"High Priority     : {high_priority}")
    print(f"Completion Rate   : {percentage:.1f}%")

    pause()

# STATISTICS

def statistics():
    if not tasks:
        print("\nNo data available.")
        pause()
        return

    categories = {}
    priorities = {}

    for task in tasks:
        category = task["category"]
        priority = task["priority"]

        categories[category] = (categories.get(category, 0) + 1)

        priorities[priority] = (priorities.get(priority, 0) + 1)

    print("\n📈 PRODUCTIVITY REPORT")
    print("------------------------------")

    print("\nCategories:")

    for category, count in categories.items():
        print(f"{category}: {count}")

    print("\nPriorities:")

    for priority, count in priorities.items():
        print(f"{priority}: {count}")

    pause()

# TASK HISTORY

def show_history():
    if not history:
        print("\nNo history available.")
        pause()
        return

    print("\n📜 TASK HISTORY")
    print("------------------------------")

    for item in reversed(history):
        print(f"{item['date']} - {item['action']}")
    pause()

# CSV EXPORT

def export_csv():
    if not tasks:
        print("\nNo tasks available to export.")
        pause()
        return

    print("\n📤 EXPORT TASKS")
    print("------------------------------")
    print("1. Export All Tasks")
    print("2. Export by Due Date Range")
    print("3. Export by Created Date Range")
    print("4. Export Today's Tasks")
    print("5. Export Completed Tasks")
    print("6. Export Pending Tasks")
    print("7. Export by Category")
    print("8. Cancel")

    choice = input("\nChoose an option: ")

    selected_tasks = []

    if choice == "1":
        selected_tasks = tasks
        file_name = "tasks_export.csv"

    elif choice == "2":
        start = get_export_date("Enter Start Date (DD-MM-YYYY): ")

        end = get_export_date("Enter End Date (DD-MM-YYYY): ")

        if start > end:
            print("\nStart date cannot be after end date.")
            pause()
            return

        for task in tasks:
            due = datetime.strptime(
                task["due_date"],
                "%d-%m-%Y"
            ).date()

            if start <= due <= end:
                selected_tasks.append(task)

        file_name = (
            f"tasks_due_"
            f"{start.strftime('%d-%m-%Y')}"
            f"_to_"
            f"{end.strftime('%d-%m-%Y')}.csv"
        )

    elif choice == "3":
        start = get_export_date("Enter Start Date (DD-MM-YYYY): ")

        end = get_export_date("Enter End Date (DD-MM-YYYY): ")

        if start > end:
            print("\nStart date cannot be after end date.")
            pause()
            return

        for task in tasks:
            created = datetime.strptime(
                task["created_date"],
                "%d-%m-%Y"
            ).date()

            if start <= created <= end:
                selected_tasks.append(task)

        file_name = (
            f"tasks_created_"
            f"{start.strftime('%d-%m-%Y')}"
            f"_to_"
            f"{end.strftime('%d-%m-%Y')}.csv"
        )

    elif choice == "4":
        today = date.today()

        for task in tasks:
            due = datetime.strptime(task["due_date"],"%d-%m-%Y").date()

            if due == today:
                selected_tasks.append(task)

        file_name = "tasks_today.csv"

    elif choice == "5":
        selected_tasks = [
            task for task in tasks
            if task["done"]
        ]

        file_name = "completed_tasks.csv"

    elif choice == "6":
        selected_tasks = [
            task for task in tasks
            if not task["done"]
        ]
        file_name = "pending_tasks.csv"

    elif choice == "7":
        category = input("Enter Category: ").strip().lower()

        selected_tasks = [
            task for task in tasks
            if task["category"].lower() == category
        ]

        file_name = f"{category}_tasks.csv"

    elif choice == "8":
        print("\nExport cancelled.")
        pause()
        return

    else:
        print("\nInvalid option.")
        pause()
        return

    if not selected_tasks:
        print("\nNo tasks found for the selected option.")
        pause()
        return

    print(f"\nFound {len(selected_tasks)} task(s).")

    confirm = input("Export these tasks? (y/n): ").lower()

    if confirm != "y":
        print("\nExport cancelled.")
        pause()
        return

    with open(
        file_name,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=selected_tasks[0].keys()
        )

        writer.writeheader()
        writer.writerows(selected_tasks)

    print("\nTasks exported successfully! 📤")
    print(f"File: {file_name}")

    pause()

# BACKUP

def create_backup():
    if not os.path.exists(FILE):
        print("\nNo task data available.")
        pause()
        return

    shutil.copy(FILE,BACKUP_FILE)

    print(f"\nBackup created: {BACKUP_FILE} 💾")

    pause()

# MAIN PROGRAM

tasks = load_tasks()
history = load_history()

while True:
    clear_screen()

    print("📝 TASK MANAGEMENT SYSTEM")
    print()
    print("01. ➕ Add Task")
    print("02. 📋 View Tasks")
    print("03. ✏️ Edit Task")
    print("04. ✅ Complete Task")
    print("05. 🔄 Mark Pending")
    print("06. 🗑️ Delete Task")
    print("07. 🔎 Search Task")
    print("08. 🔍 Filter Tasks")
    print("09. 📊 Dashboard")
    print("10. 📈 Statistics")
    print("11. 📜 Task History")
    print("12. 📤 Export Tasks")
    print("13. 💾 Create Backup")
    print("14. 🚪 Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        edit_task()

    elif choice == "4":
        complete_task()

    elif choice == "5":
        mark_pending()

    elif choice == "6":
        delete_task()

    elif choice == "7":
        search_task()

    elif choice == "8":
        filter_tasks()

    elif choice == "9":
        dashboard()

    elif choice == "10":
        statistics()

    elif choice == "11":
        show_history()

    elif choice == "12":
        export_csv()

    elif choice == "13":
        create_backup()

    elif choice == "14":
        save_tasks()
        save_history()
        print("\nGoodbye! 👋")
        break

    else:
        print("\nInvalid Option!")
        pause()