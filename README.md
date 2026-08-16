# PyTasker

### Python Task Management & Productivity System

PyTasker is a Python-based command-line task management application for organizing tasks, tracking deadlines, managing priorities, and monitoring productivity. It uses JSON for persistent storage and provides search, filtering, task history, CSV export, statistics, and backup functionality.

---

## Features

- ➕ Add, edit, and delete tasks
- ✅ Mark tasks as completed or pending
- 📅 Organize tasks by due date
- ⚠️ Track overdue, today, tomorrow, and upcoming tasks
- 🎯 Manage priorities and categories
- 🏷️ Add descriptions and tags
- 🔎 Search tasks by keywords
- 🔍 Filter tasks by status, priority, date, and category
- 📊 View productivity dashboard and statistics
- 📜 Maintain task history
- 📤 Export tasks to CSV
- 📅 Export tasks using date ranges
- 💾 Create task backups

---

## Application Menu

```text
📝 TASK MANAGEMENT SYSTEM

01. ➕ Add Task
02. 📋 View Tasks
03. ✏️ Edit Task
04. ✅ Complete Task
05. 🔄 Mark Pending
06. 🗑️ Delete Task
07. 🔎 Search Task
08. 🔍 Filter Task
09. 📊 Dashboard
10. 📈 Statistics
11. 📜 Task History
12. 📤 Export Tasks
13. 💾 Create Backup
14. 🚪 Exit
```

---

## Task Organization

Tasks are automatically categorized based on their status and deadlines.

```text
📋 TASK LIST
------------------------------

⚠️ OVERDUE
------------------------------

📅 TODAY
------------------------------

🌅 TOMORROW
------------------------------

📆 UPCOMING
------------------------------

✅ COMPLETED
------------------------------
```

### Each Task Stores

```text
ID
Task
Description
Priority
Category
Tags
Created Date
Due Date
Status
```

---

## Technology

| Technology | Purpose |
|---|---|
| Python | Application development |
| JSON | Persistent data storage |
| CSV | Data export |
| datetime | Date and deadline management |
| os | File and system operations |
| shutil | Backup management |

No external Python packages are required.

---

## Project Structure

```text
PyTasker/
│
├── PyTasker.py
├── tasks.json
├── task_history.json
├── README.md
└── .gitignore
```

### Runtime-Generated Files

```text
tasks_backup.json
tasks_export.csv
```

---

## Data Flow

```text
User
  ↓
PyTasker
  ↓
Task Management
  ↓
JSON Storage
  ↓
Search / Filter / Statistics
  ↓
CSV Export / Backup
```

---

## Future Enhancements

- 🖥️ GUI version
- 🗄️ MySQL database integration
- 👤 User authentication
- 🔔 Task reminders
- 📊 Advanced charts
- 🐼 Pandas-based analytics
- 🌐 Web application
- ☁️ Cloud storage

---
