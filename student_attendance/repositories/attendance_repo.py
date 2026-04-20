from models.attendance import Attendance
from repositories.db import get_connection


class AttendanceRepo:
    def get_session(self, session_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM session WHERE session_id = ?", (session_id,)).fetchone()
        conn.close()
        return row

    def update_session_status(self, session_id, is_open):
        conn = get_connection()
        conn.execute("UPDATE session SET is_open = ? WHERE session_id = ?", (int(is_open), session_id))
        conn.commit()
        conn.close()

    def get_attendance(self, session_id, student_id):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT attendance_id, session_id, student_id, status, recorded_at
            FROM attendance
            WHERE session_id = ? AND student_id = ?
            """,
            (session_id, student_id),
        ).fetchone()
        conn.close()
        return self._to_attendance(row)

    def insert_attendance(self, attendance):
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO attendance (attendance_id, session_id, student_id, status, recorded_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                attendance.attendance_id,
                attendance.session_id,
                attendance.student_id,
                int(attendance.status),
                attendance.recorded_at,
            ),
        )
        conn.commit()
        conn.close()

    def update_attendance(self, session_id, student_id, status, recorded_at):
        conn = get_connection()
        conn.execute(
            """
            UPDATE attendance
            SET status = ?, recorded_at = ?
            WHERE session_id = ? AND student_id = ?
            """,
            (int(status), recorded_at, session_id, student_id),
        )
        conn.commit()
        conn.close()

    def get_attendance_by_session(self, session_id):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT
                a.attendance_id,
                a.session_id,
                a.student_id,
                a.status,
                a.recorded_at,
                u.full_name AS student_name,
                c.class_name
            FROM attendance a
            JOIN student s ON s.student_id = a.student_id
            JOIN users u ON u.user_id = s.user_id
            JOIN session se ON se.session_id = a.session_id
            JOIN class c ON c.class_id = se.class_id
            WHERE a.session_id = ?
            ORDER BY a.student_id
            """,
            (session_id,),
        ).fetchall()
        conn.close()
        return [self._to_attendance(row) for row in rows]

    def get_attendance_by_student(self, student_id):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT
                a.attendance_id,
                a.session_id,
                a.student_id,
                a.status,
                a.recorded_at,
                u.full_name AS student_name,
                c.class_name
            FROM attendance a
            JOIN student s ON s.student_id = a.student_id
            JOIN users u ON u.user_id = s.user_id
            JOIN session se ON se.session_id = a.session_id
            JOIN class c ON c.class_id = se.class_id
            WHERE a.student_id = ?
            ORDER BY a.recorded_at DESC
            """,
            (student_id,),
        ).fetchall()
        conn.close()
        return [self._to_attendance(row) for row in rows]

    def is_student_in_class(self, student_id, class_id):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT 1
            FROM class_student
            WHERE student_id = ? AND class_id = ?
            """,
            (student_id, class_id),
        ).fetchone()
        conn.close()
        return row is not None

    def get_class_id_by_session(self, session_id):
        conn = get_connection()
        row = conn.execute("SELECT class_id FROM session WHERE session_id = ?", (session_id,)).fetchone()
        conn.close()
        return row["class_id"] if row else None

    def _to_attendance(self, row):
        if not row:
            return None
        return Attendance(
            attendance_id=row["attendance_id"],
            session_id=row["session_id"],
            student_id=row["student_id"],
            status=row["status"],
            recorded_at=row["recorded_at"],
            student_name=row["student_name"] if "student_name" in row.keys() else None,
            class_name=row["class_name"] if "class_name" in row.keys() else None,
        )
