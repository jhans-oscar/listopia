# Listopia v2 – Task Tracker CLI

**Tagline:** Because even chaos deserves a list. ✅

## Demo

No ready yet - sorry

## Installation

```bahs
git clone https://github.com/jhans-oscar/listopia.git

cd listopia
python3 listopia_v2.py
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


## Inspiration

This project was inspired by the task tracker idea on [Roadmap.sh](https://roadmap.sh/projects/task-tracker).
