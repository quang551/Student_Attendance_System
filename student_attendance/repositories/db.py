import sqlite3

DB_NAME = "attendance.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        user_name TEXT,
        full_name TEXT,
        password TEXT,
        email TEXT,
        role INTEGER
    )
    """)

    # ADMIN
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        admin_id TEXT PRIMARY KEY,
        user_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # STUDENT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        student_id TEXT PRIMARY KEY,
        user_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # LECTURER
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lecturer (
        lecturer_id TEXT PRIMARY KEY,
        user_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # COURSE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course (
        course_id TEXT PRIMARY KEY,
        course_name TEXT,
        description TEXT
    )
    """)

    # CLASS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class (
        class_id TEXT PRIMARY KEY,
        class_name TEXT,
        course_id TEXT,
        lecturer_id TEXT,
        FOREIGN KEY (course_id) REFERENCES course(course_id),
        FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
    )
    """)

    # CLASS-STUDENT (many-to-many)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_student (
        classStudent_id TEXT PRIMARY KEY,
        student_id TEXT,
        class_id TEXT,
        FOREIGN KEY (student_id) REFERENCES student(student_id),
        FOREIGN KEY (class_id) REFERENCES class(class_id)
    )
    """)

    # SESSION
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS session (
        session_id TEXT PRIMARY KEY,
        class_id TEXT,
        start_time TEXT,
        end_time TEXT,
        is_open TEXT,
        FOREIGN KEY (class_id) REFERENCES class(class_id)
    )
    """)

    # ATTENDANCE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id TEXT PRIMARY KEY,
        session_id TEXT,
        student_id TEXT,
        status INTEGER,
        recorded_at TEXT,
        FOREIGN KEY (session_id) REFERENCES session(session_id),
        FOREIGN KEY (student_id) REFERENCES student(student_id)
    )
    """)

    conn.commit()
    conn.close()