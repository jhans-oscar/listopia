#!/usr/bin/env python3

import sys
import os
import json
from datetime import datetime 

ALLOWED_STATUSES = ["todo", "in-progress", "done"]
DATAFILE = os.path.join(os.path.dirname(__file__), "tasks.json")

# --- Low Level Functions ---

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
        "updatedAt": now
    }

def validate_description(description):
    if not description or not description.strip():
        raise ValueError("Error: Task description is required")
    return description.strip()

def format_task(task):
    return (f"[{task['id']}] {task['description']} "
            f"({task['status']})\n  Created: {task['createdAt']}\n  Updated: {task['updatedAt']}")

def find_task_by_id(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

# --- High Level Functions ---

def add_task(description):
    description = validate_description(description)
    tasks = load_tasks()
    new_id = generate_task_id(tasks)
    new_task = create_task(description, new_id)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Task added successfully (ID: {new_id}): {description}")

def list_tasks(status_filter=None):
    tasks = load_tasks()
    if status_filter:
        if status_filter not in ALLOWED_STATUSES:
            print(f"Error: Status must be one of {ALLOWED_STATUSES}")
            sys.exit(1)
        tasks = [t for t in tasks if t["status"] == status_filter]

    if not tasks:
        if status_filter:
            print(f"No tasks found with status '{status_filter}'")
        else:
            print("No tasks found")
        return

    # Deterministic ordering by id
    tasks = sorted(tasks, key=lambda t: t.get("id", 0))
    print("📋 Tasks:")
    for task in tasks:
        print(format_task(task))
        print("-" * 40)

def update_task(task_id, new_description):
    description = validate_description(new_description)
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if not task:
        print(f"No task found with ID {task_id}")
        sys.exit(1)

    task["description"] = description
    task["updatedAt"] = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"✅ Task {task_id} updated successfully: {description}")

# --- Main CLI ---

def main():
    if len(sys.argv) < 2:
        prog = os.path.basename(sys.argv[0])
        print(f"Usage: {prog} <command> [args]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) >= 3:
            try:
                add_task(" ".join(sys.argv[2:]))
            except ValueError as e:
                print(str(e))
                sys.exit(1)
        else:
            print("Error: Task description is required")
            sys.exit(1)

    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        elif len(sys.argv) == 3:
            status_filter = sys.argv[2].lower()
            list_tasks(status_filter)
        else:
            print("Error: Too many arguments for 'list'. Usage: list [status]")
            sys.exit(1)

    elif command == "update":
        if len(sys.argv) >= 4:
            task_id_str = sys.argv[2]
            if not task_id_str.isdigit():
                print("Error: Task ID must be a number")
                sys.exit(1)
            task_id = int(task_id_str)
            new_description = " ".join(sys.argv[3:])
            try:
                update_task(task_id, new_description)
            except ValueError as e:
                print(str(e))
                sys.exit(1)
        else:
            print("Error: Task ID and new task description are required")
            sys.exit(1)

    elif command == "delete":
        if len(sys.argv) >= 3:
            task_id_str = sys.argv[2]
            if not task_id_str.isdigit():
                print("Error: Task ID must be a number")
                sys.exit(1)
            task_id = int(task_id_str)
            tasks = load_tasks()
            task = find_task_by_id(tasks, task_id)
            if task:
                tasks.remove(task)
                save_tasks(tasks)
                print(f"✅ Task {task_id} deleted successfully")
            else:
                print(f"No task found with ID {task_id}")
                sys.exit(1)
        else:
            print("Error: Task ID is required")
            sys.exit(1)

    elif command == "status":
        if len(sys.argv) >= 4:
            task_id_str = sys.argv[2]
            if not task_id_str.isdigit():
                print("Error: Task ID must be a number")
                sys.exit(1)
            task_id = int(task_id_str)
            new_status = sys.argv[3].lower()
            if new_status not in ALLOWED_STATUSES:
                print(f"Error: Status must be one of {ALLOWED_STATUSES}")
                sys.exit(1)
            tasks = load_tasks()
            task = find_task_by_id(tasks, task_id)
            if task:
                task["status"] = new_status
                task["updatedAt"] = datetime.now().isoformat()
                save_tasks(tasks)
                print(f"✅ Task {task_id} status updated to {new_status}")
            else:
                print(f"No task found with ID {task_id}")
                sys.exit(1)
        else:
            print("Error: Task ID and new status are required")
            sys.exit(1)

    else:
        prog = os.path.basename(sys.argv[0])
        print("Invalid command")
        print(f"Usage: {prog} <command> [args]")
        print("Commands: add <desc> | list [status] | update <id> <desc> | delete <id> | status <id> <status>")
        sys.exit(1)

if __name__ == "__main__":
    main()
