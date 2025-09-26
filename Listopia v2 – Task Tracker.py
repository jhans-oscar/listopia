#!/usr/bin/env python3

import os
import json
import time
from datetime import datetime 

ALLOWED_STATUSES = ["todo", "in-progress", "done"]
DATAFILE = os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), "tasks.json")

# --- Low Level Functions ---
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
def main_menu():
    print("=" * 40)
    print("         🗂️  TASK TRACKER CLI")
    print("=" * 40)
    print("1) ➕ Add Task")
    print("2) 📋 View Tasks")
    print("3) ✏️  Update Task")
    print("4) 🗑️  Delete Task")
    print("5) 🔄 Change Task Status")
    print("6) 🚪 Exit")
    print("=" * 40)
    
    choice = input("Select an option (1-6): ")
    return choice

def load_tasks():
    if not os.path.exists(DATAFILE):
        with open(DATAFILE, 'w') as f:
            json.dump([], f)
        return []

    with open(DATAFILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Backup the corrupted file before resetting to empty
            try:
                backup_path = DATAFILE + ".bak"
                os.replace(DATAFILE, backup_path)
                print(f"Warning: Corrupted JSON detected. Backed up to: {backup_path}. Starting with an empty task list.")
            except Exception:
                print("Warning: Corrupted JSON file. Could not create backup. Starting with an empty task list.")
            with open(DATAFILE, 'w') as wf:
                json.dump([], wf)
            return []

def save_tasks(tasks):
    with open(DATAFILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def generate_task_id(tasks):
    if not tasks:
        return 1
    max_id = max(task["id"] for task in tasks)
    return max_id + 1

def create_task(description, task_id):
    now = datetime.now().isoformat()
    return {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": None
    }

def validate_description(description):
    if not description or not description.strip():
        raise ValueError("Error: Task description is required")
    return description.strip()

def _format_datetime(dt_string):
    if not dt_string:
        return "—"
    try:
        # Expecting ISO format; fall back to raw string if parse fails
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%b %d, %Y %H:%M")
    except Exception:
        return dt_string

def _status_badge(status):
    badges = {
        "todo": "📝",
        "in-progress": "🚧",
        "done": "✅",
    }
    return badges.get(status, "🔖")

def _status_label(status):
    return f"{_status_badge(status)} {status}"

def _truncate(text, width):
    if text is None:
        return ""
    text = str(text)
    return text if len(text) <= width else text[: max(0, width - 1)] + "…"

def format_task(task):
    # Column widths
    id_w = 4
    desc_w = 44
    status_w = 14
    time_w = 17  # e.g., 'Sep 26, 2025 14:03'

    task_id = f"{task.get('id', ''):>{id_w}}"
    description = _truncate(task.get('description', ''), desc_w)
    status = _truncate(_status_label(task.get('status', '')), status_w)
    created_str = _truncate(_format_datetime(task.get('createdAt')), time_w)
    updated_str = _truncate(_format_datetime(task.get('updatedAt')), time_w)

    return (
        f"{task_id}  "
        f"{description:<{desc_w}}  "
        f"{status:<{status_w}}  "
        f"{created_str:<{time_w}}  "
        f"{updated_str:<{time_w}}"
    )

def _print_table(tasks, title):
    id_w = 4
    desc_w = 44
    status_w = 14
    time_w = 17

    print(title)
    header = (
        f"{'ID':>{id_w}}  "
        f"{'Task':<{desc_w}}  "
        f"{'Status':<{status_w}}  "
        f"{'Created':<{time_w}}  "
        f"{'Updated':<{time_w}}"
    )
    print(header)
    print("-" * len(header))
    for task in tasks:
        print(format_task(task))

def find_task_by_id(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def set_task_status(task, new_status):
    if new_status not in ALLOWED_STATUSES:
        raise ValueError(f"Status must be one of {ALLOWED_STATUSES}")
    task["status"] = new_status
    task["updatedAt"] = datetime.now().isoformat()

def get_tasks_by_status(tasks, status):
    return [task for task in tasks if task.get("status") == status]

def reindex_task_ids(tasks):
    # Ensure stable order by current id, then assign sequential IDs starting at 1
    tasks.sort(key=lambda t: t.get("id", 0))
    for index, task in enumerate(tasks, start=1):
        task["id"] = index
    return tasks


# --- High Level Functions ---

def add_task(description):
    description = validate_description(description)
    tasks = load_tasks()
    new_id = generate_task_id(tasks)
    new_task = create_task(description, new_id)
    tasks.append(new_task)
    save_tasks(tasks)
    print("\n✅ Task added successfully!\n")
    time.sleep(2)
    print(format_task(new_task))

def list_tasks():
    clear_screen()
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found. Use 'Add Task' to create your first task.")
        time.sleep(2)
    else:
        sorted_tasks = sorted(tasks, key=lambda t: t.get("id", 0))
        print()
        _print_table(sorted_tasks, f"📋 All Tasks · {len(sorted_tasks)} item(s)")

    input("\nPress Enter to return to menu...")


def list_tasks_by_status():
    status = input(f"Enter status to filter {ALLOWED_STATUSES}: ").lower()
    if status not in ALLOWED_STATUSES:
        print(f"Error: status must be one of {ALLOWED_STATUSES}")
        time.sleep(2)
        return
    
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found. Use 'Add Task' to create your first task.")
        time.sleep(2)
        return

    filtered = sorted(get_tasks_by_status(tasks, status), key=lambda t: t.get("id", 0))
    if not filtered:
        print(f"📭 No tasks found with status '{status}'.")
        time.sleep(2)
        return

    print()
    _print_table(filtered, f"📋 {status.title()} Tasks · {len(filtered)} item(s):")

    input("\nPress Enter to return to menu...")

def update_task(task_id, new_description):
    description = validate_description(new_description)
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if not task:
        print(f"No task found with ID {task_id}")
        time.sleep(2)
        return

    print("\n📝 Updating the following task:\n")
    print(format_task(task))
    print("-" * 40)


    confirm = input("Proceed with update? (y/n): ").strip().lower()
    if confirm != "y":
        print("Update cancelled.")
        time.sleep(2)
        return

    task["description"] = description
    task["updatedAt"] = datetime.now().isoformat()
    save_tasks(tasks)
    print("\n✅ Task updated successfully!\n")
    print(format_task(task))
    time.sleep(2)

def delete_task(task_id):
    if not task_id.isdigit():
        print("Error: Task ID must be a number")
        time.sleep(2)
        return

    task_id = int(task_id)
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    if task:
        print("\n🗑️  The following task will be deleted:\n")
        print(format_task(task))
        print("-" * 40)
        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm != "y":
            print("Deletion cancelled.")
            time.sleep(2)
            return
        tasks.remove(task)
        reindex_task_ids(tasks)
        save_tasks(tasks)
        print(f"✅ Task {task_id} deleted successfully. IDs reindexed.")
        time.sleep(2)

def update_task_status():
        try:
            task_id = int(input("Enter task ID to update status: "))
        except ValueError:
            print("Task ID must be a number")
            time.sleep(2)
            return
                          
        tasks = load_tasks()
        task = find_task_by_id(tasks, task_id)
        if not task:
            print(f"No task found with ID {task_id}")
            time.sleep(2)
            return
        
        print("\n📝 Current task before status change:\n")
        print(format_task(task))
        print("-" * 40)

        new_status = input(f"Enter new status {ALLOWED_STATUSES}: ").lower()
        if new_status not in ALLOWED_STATUSES:
            print(f"Error: Status must be one of {ALLOWED_STATUSES}")
            time.sleep(2)
            return 
        
        task["status"] = new_status
        task["updatedAt"] = datetime.now().isoformat()
        save_tasks(tasks)
        print("\n✅ Status updated successfully!\n")
        print(format_task(task))
        time.sleep(2)


    
# --- Main CLI ---

def main():
    while True:
        clear_screen()
        choice = main_menu()

        if choice == "1": # Add New Task

            description = input("Enter task description:  ")

            try:
                add_task(description)

            except ValueError as e:
                print(str(e))

        elif choice == "2": # View Tasks (all or filtered)

            filter_choice = input("Do you want to filter by status? (y/n): ").lower()

            if filter_choice == "y":
                list_tasks_by_status()

            else:
                list_tasks()  

        elif choice == "3":
                try:
                    task_id = int(input("Enter task ID to update: "))
                except ValueError :
                    print("Error: Task ID must be a number")
                    continue

                new_desc = input("Enter new task description: ")
                try:
                    update_task(task_id, new_desc)
                except ValueError as e:
                    print(str(e))


        elif choice == "4":
                
                task_id = input("Enter task ID to delete: ")

                try:
                    delete_task(task_id)

                except ValueError as e:
                    print(str(e))
                
        elif choice == "5":
            update_task_status()

        elif choice == "6":
            print("\n👋 Goodbye!\n")
            quit()
  

        else:
            print("❌ Invalid choice. Please select a valid menu option.")


if __name__ == "__main__":
    main()