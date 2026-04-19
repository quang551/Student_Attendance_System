from repositories.db import get_connection
from models.attendance import Attendance

# ==============================
# SESSION
# ==============================
def create_session(session_id, class_id, start_time, end_time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO session (session_id, class_id, start_time, end_time, is_open)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, class_id, start_time, end_time, "0"))

    conn.commit()
    conn.close()


def update_session_status(session_id, is_open):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE session
        SET is_open = ?
        WHERE session_id = ?
    """, (is_open, session_id))

    conn.commit()
    conn.close()


def get_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM session WHERE session_id = ?
    """, (session_id,))

    result = cursor.fetchone()
    conn.close()

    return result


# ==============================
# ATTENDANCE
# ==============================
def get_attendance(session_id, student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendance
        WHERE session_id = ? AND student_id = ?
    """, (session_id, student_id))

    result = cursor.fetchone()
    conn.close()

    return result


def insert_attendance(attendance_id, session_id, student_id, status, recorded_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance (attendance_id, session_id, student_id, status, recorded_at)
        VALUES (?, ?, ?, ?, ?)
    """, (attendance_id, session_id, student_id, status, recorded_at))

    conn.commit()
    conn.close()


def update_attendance(session_id, student_id, status, recorded_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE attendance
        SET status = ?, recorded_at = ?
        WHERE session_id = ? AND student_id = ?
    """, (status, recorded_at, session_id, student_id))

    conn.commit()
    conn.close()


def get_attendance_by_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attendance_id, session_id, student_id, status, recorded_at
        FROM attendance
        WHERE session_id = ?
    """, (session_id,))

    rows = cursor.fetchall()
    conn.close()

    return [Attendance(*row) for row in rows]

def get_attendance_by_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attendance_id, session_id, student_id, status, recorded_at
        FROM attendance
        WHERE student_id = ?
    """, (student_id,))

    rows = cursor.fetchall()
    conn.close()

    return [Attendance(*row) for row in rows]

def is_student_in_class(student_id, class_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM class_student
        WHERE student_id = ? AND class_id = ?
    """, (student_id, class_id))

    result = cursor.fetchone()
    conn.close()

    return result is not None

def get_class_id_by_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT class_id FROM session WHERE session_id = ?
    """, (session_id,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None