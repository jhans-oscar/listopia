# Listopia v2 – Task Tracker CLI

**Tagline:** Because even chaos deserves a list. ✅

## Demo

No ready yet - sorry

## Installation

Clone the repository and run with Python 3:

```python
git clone https://github.com/jhans-oscar/task-tracker-cli
cd task-tracker-cli
python3 task_tracker_v1.py <command> [args]
```

No external dependencies are required.

## Usage

Clone the repo:

```bash
git clone https://github.com/jhans-oscar/listopia.git
cd listopia
```

Run the CLI:

```bash
python3 task_tracker_cli_v2.py
```


## Commands / CLI Usage

| Command         | Description                                            |
| --------------- | ------------------------------------------------------ |
| add             | Add a new task                                         |
| list            | Show all tasks                                         |
| list (filtered) | Filter tasks by status (`todo`, `in-progress`, `done`) |
| update          | Update task description by ID                          |
| delete          | Delete a task by ID                                    |
| status          | Change a task’s status                                 |



## File Storage

All tasks are stored in tasks.json.
If the file is corrupted, the program creates a backup (tasks.json.bak) before resetting it.

---

## Inspiration

This project was inspired by the task tracker idea on [Roadmap.sh](https://roadmap.sh/projects/task-tracker).
