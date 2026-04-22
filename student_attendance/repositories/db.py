import hashlib
import sqlite3
from pathlib import Path
import os


ROOT_DIR = Path(__file__).resolve().parent.parent

DB_PATH = os.getenv("DB_PATH")

if DB_PATH:
    DB_NAME = Path(DB_PATH)
else:
    DB_NAME = ROOT_DIR / "attendance.db"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection():
    conn = sqlite3.connect(str(DB_NAME))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            user_name TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'lecturer', 'student'))
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS admin (
            admin_id TEXT PRIMARY KEY,
            user_id TEXT UNIQUE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lecturer (
            lecturer_id TEXT PRIMARY KEY,
            user_id TEXT UNIQUE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student (
            student_id TEXT PRIMARY KEY,
            user_id TEXT UNIQUE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS course (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            description TEXT DEFAULT ''
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS class (
            class_id TEXT PRIMARY KEY,
            class_name TEXT NOT NULL,
            course_id TEXT NOT NULL,
            lecturer_id TEXT,
            FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE RESTRICT,
            FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id) ON DELETE SET NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS class_student (
            classStudent_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            class_id TEXT NOT NULL,
            UNIQUE(student_id, class_id),
            FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
            FOREIGN KEY (class_id) REFERENCES class(class_id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS session (
            session_id TEXT PRIMARY KEY,
            class_id TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            is_open INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (class_id) REFERENCES class(class_id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            student_id TEXT NOT NULL,
            status INTEGER NOT NULL CHECK (status IN (1, 2, 3)),
            recorded_at TEXT NOT NULL,
            UNIQUE(session_id, student_id),
            FOREIGN KEY (session_id) REFERENCES session(session_id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute("SELECT user_id, password FROM users")
    for row in cursor.fetchall():
        password = row["password"]
        if not _looks_hashed(password):
            cursor.execute(
                "UPDATE users SET password = ? WHERE user_id = ?",
                (hash_password(password), row["user_id"]),
            )

    cursor.execute("SELECT COUNT(*) AS total FROM users")
    if cursor.fetchone()["total"] == 0:
        cursor.execute(
            """
            INSERT INTO users (user_id, user_name, full_name, password, email, role)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "U001",
                "admin01",
                "Administrator",
                hash_password("admin123"),
                "admin@example.com",
                "admin",
            ),
        )
        cursor.execute("INSERT INTO admin (admin_id, user_id) VALUES (?, ?)", ("A001", "U001"))

    conn.commit()
    conn.close()


def _looks_hashed(value: str) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(ch in "0123456789abcdef" for ch in value.lower())
