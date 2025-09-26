# Task Tracker (CLI)

A simple command-line task manager written in Python.
You can add, list, update, delete, and change the status of tasks.
Tasks are stored locally in a JSON file (tasks.json).

## Features

- List tasks, optionally filtered by status (todo, in-progress, done).

- Update a task’s description.

- Delete tasks by ID.

- Change the status of a task.

- Auto-generates unique IDs for tasks.

- Handles corrupted JSON by creating a backup.

## Installation

Clone the repository and run with Python 3:

```python
git clone https://github.com/yourusername/task-tracker.git
cd task-tracker
python3 task_tracker_v1.py <command> [args]
```

No external dependencies are required.

## Usage

```bash
python3 task_tracker_v1.py <command> [args]
```

### Commands

- Add a task

```bash
python3 task_tracker_v1.py add "Buy milk"
```

- List all tasks

```bash
python3 task_tracker_v1.py list
```

- List only tasks with a specific status

```bash
python3 task_tracker_v1.py list done
```

- Update a task description

```bash
python3 task_tracker_v1.py update 1 "Buy milk and eggs"
```

- Delete a task

```bash
python3 task_tracker_v1.py delete 1
```

- Change a task's status

```bash
python3 task_tracker_v1.py status 2 in-progress
```

## File Storage

All tasks are stoed in tasks.json.
If the file is corrupted, the program creates a backup (tasks.json.bak) before resetting it.

## Example

```bash
$ python3 task_tracker_v1.py add "Learn Python"
✅ Task added successfully (ID: 1): Learn Python

$ python3 task_tracker_v1.py list
📋 Tasks:
[1] Learn Python (todo)
  Created: 2025-09-26T12:00:00
  Updated: 2025-09-26T12:00:00
----------------------------------------
```

