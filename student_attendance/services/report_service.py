from student_attendance.repositories.class_repo import ClassRepo
from student_attendance.repositories.db import get_connection
from student_attendance.repositories.user_repo import UserRepo


class ReportService:
    def __init__(self, class_repo=None, user_repo=None):
        self.class_repo = class_repo or ClassRepo()
        self.user_repo = user_repo or UserRepo()

    def list_students_for_report(self):
        return self.user_repo.list_all("student")

    def report_by_class(self, class_id):
        current_class = self.class_repo.find_by_id(class_id)
        if not current_class:
            return False, "Class not found!", None

        conn = get_connection()
        rows = conn.execute(
            """
            SELECT a.status
            FROM attendance a
            JOIN session s ON s.session_id = a.session_id
            WHERE s.class_id = ?
            """,
            (class_id,),
        ).fetchall()
        conn.close()

        return True, "OK", self._build_report(rows)

    def report_by_student(self, student_id):
        student = self.user_repo.get_role_user("student", student_id)
        if not student:
            return False, "Student not found!", None

        conn = get_connection()
        rows = conn.execute(
            """
            SELECT status
            FROM attendance
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchall()
        conn.close()

        return True, "OK", self._build_report(rows)

    def _build_report(self, rows):
        total = len(rows)
        present = sum(1 for row in rows if row["status"] == 1)
        absent = sum(1 for row in rows if row["status"] == 2)
        late = sum(1 for row in rows if row["status"] == 3)
        rate = (present / total * 100) if total else 0
        return {
            "total": total,
            "present": present,
            "absent": absent,
            "late": late,
            "rate": round(rate, 2),
        }
