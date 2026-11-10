import os
import sqlite3
import mysql.connector

class SQLiteCursorWrapper:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def execute(self, query, params=None):
        # Convert MySQL %s placeholder to SQLite ? placeholder
        sqlite_query = query.replace("%s", "?")
        # Replace CURDATE() with date('now')
        sqlite_query = sqlite_query.replace("CURDATE()", "date('now')")
        if params is not None:
            return self.cursor.execute(sqlite_query, params)
        else:
            return self.cursor.execute(sqlite_query)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

class DBWrapper:
    def __init__(self):
        self.use_mysql = False
        self.conn = None
        self._connect()

    def _connect(self):
        host = os.environ.get("DB_HOST", "localhost")
        user = os.environ.get("DB_USER", "root")
        password = os.environ.get("DB_PASSWORD", "mohan123")
        database = os.environ.get("DB_NAME", "project")
        
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                connect_timeout=3
            )
            self.use_mysql = True
            print("Connected to MySQL database")
        except Exception as e:
            print("MySQL connection failed, falling back to SQLite:", e)
            db_path = os.path.join(os.path.dirname(__file__), "project.db")
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.use_mysql = False
            self._init_sqlite()

    def _init_sqlite(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            role_id TEXT,
            email TEXT,
            phone TEXT,
            user_type TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            dob TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            department TEXT,
            designation TEXT,
            joining_date TEXT,
            salary REAL,
            status TEXT,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_delete INTEGER DEFAULT 0,
            role_id TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS attendances (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            attendance_date TEXT,
            check_in TEXT,
            check_out TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_delete INTEGER DEFAULT 0
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS leaves (
            leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            leave_type TEXT,
            from_date TEXT,
            to_date TEXT,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_delete INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Pending',
            approved_by TEXT,
            approved_date TEXT,
            remarks TEXT
        )''')
        self.conn.commit()

    def cursor(self):
        if self.use_mysql:
            return self.conn.cursor()
        else:
            return SQLiteCursorWrapper(self.conn)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

db = DBWrapper()
cursor = db.cursor()
