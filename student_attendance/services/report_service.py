from repositories.db import get_connection


class ReportService:
    def report_by_class(self, class_id):
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
        return self._build_report(rows)

    def report_by_student(self, student_id):
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
        return self._build_report(rows)

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
