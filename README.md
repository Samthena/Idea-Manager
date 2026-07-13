# Idea Manager

Idea Manager is a simple web app for tracking ideas and client requests. It lets you add, view, search, filter, update, and delete ideas.

## What you need

Before you start, make sure you have:
- Python 3.10 or newer
- Git
- A terminal or command prompt

## 1. Clone the project

Open a terminal and run:

```bash
git clone <your-repository-url>
cd Idea-Manager
```

## 2. Create a virtual environment

This keeps the app dependencies separate from the rest of your system.

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

## 4. Run the app

Start the app with:

```bash
python Omnilinx.py
```

Then open your browser and go to:

```text
http://127.0.0.1:5000/
```

## 5. Shared database setup for multiple users

This app uses SQLite. To make the database available to multiple people on different computers, the database file should be stored in a shared location such as a network drive, shared folder, or cloud-synced folder.

For example, create a folder like this:

```text
\\server\shared\idea-manager\db
```

Then set the database path in the app configuration to point to that shared folder.

If you want to use a single shared database file, set the app to use a full path like:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///\\\\server\\shared\\idea-manager\\db\\Ideas.db'
```

If you are using a local shared folder on the same machine, you can also use a path like:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/shared/idea-manager/db/Ideas.db'
```

> Important: all users who need to access the same database must be able to read and write to that shared folder.

## 6. Notes for multiple users

- Each person should clone the project separately.
- Everyone should install the same dependencies.
- Everyone should use the same shared database path in the configuration.
- If one person changes the database location, the others must update their local configuration too.

## 7. Troubleshooting

If the app does not start:
- make sure the virtual environment is activated
- make sure all dependencies are installed
- make sure the database path exists and is writable
- check that the port 5000 is not already in use

## 8. Example workflow

1. Clone the repo
2. Create and activate a virtual environment
3. Install requirements
4. Start the app
5. Open the browser and use the app
6. Share the same database path with other users if you want everyone to work from one data source

