from models.class_model import Class
from repositories.db import get_connection


class ClassRepo:
    def add(self, new_class):
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO class (class_id, class_name, course_id, lecturer_id)
            VALUES (?, ?, ?, ?)
            """,
            (new_class.class_id, new_class.class_name, new_class.course_id, new_class.lecturer_id),
        )
        conn.commit()
        conn.close()
        return new_class

    def get_all(self):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT class_id, class_name, course_id, lecturer_id
            FROM class
            ORDER BY class_id
            """
        ).fetchall()
        conn.close()
        return [self._to_class(row) for row in rows]

    def find_by_id(self, class_id):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT class_id, class_name, course_id, lecturer_id
            FROM class
            WHERE class_id = ?
            """,
            (class_id,),
        ).fetchone()
        conn.close()
        return self._to_class(row)

    def delete(self, class_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM class WHERE class_id = ?", (class_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def update(self, class_id, new_course_id=None, new_class_name=None, lecturer_id=None):
        current = self.find_by_id(class_id)
        if not current:
            return False

        conn = get_connection()
        conn.execute(
            """
            UPDATE class
            SET class_name = ?, course_id = ?, lecturer_id = ?
            WHERE class_id = ?
            """,
            (
                new_class_name if new_class_name is not None else current.class_name,
                new_course_id if new_course_id is not None else current.course_id,
                lecturer_id if lecturer_id is not None else current.lecturer_id,
                class_id,
            ),
        )
        conn.commit()
        conn.close()
        return True

    def list_by_lecturer(self, lecturer_id):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT class_id, class_name, course_id, lecturer_id
            FROM class
            WHERE lecturer_id = ?
            ORDER BY class_id
            """,
            (lecturer_id,),
        ).fetchall()
        conn.close()
        return [self._to_class(row) for row in rows]

    def list_by_student(self, student_id):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT c.class_id, c.class_name, c.course_id, c.lecturer_id
            FROM class c
            JOIN class_student cs ON cs.class_id = c.class_id
            WHERE cs.student_id = ?
            ORDER BY c.class_id
            """,
            (student_id,),
        ).fetchall()
        conn.close()
        return [self._to_class(row) for row in rows]

    def list_students(self, class_id):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT s.student_id, u.full_name, u.user_name, u.email
            FROM class_student cs
            JOIN student s ON s.student_id = cs.student_id
            JOIN users u ON u.user_id = s.user_id
            WHERE cs.class_id = ?
            ORDER BY s.student_id
            """,
            (class_id,),
        ).fetchall()
        conn.close()
        return rows

    def is_student_enrolled(self, class_id, student_id):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT 1
            FROM class_student
            WHERE class_id = ? AND student_id = ?
            """,
            (class_id, student_id),
        ).fetchone()
        conn.close()
        return row is not None

    def enroll_student(self, class_id, student_id, class_student_id):
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO class_student (classStudent_id, student_id, class_id)
            VALUES (?, ?, ?)
            """,
            (class_student_id, student_id, class_id),
        )
        conn.commit()
        conn.close()

    def remove_student(self, class_id, student_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM class_student WHERE class_id = ? AND student_id = ?",
            (class_id, student_id),
        )
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def _to_class(self, row):
        if not row:
            return None
        return Class(row["class_id"], row["class_name"], row["course_id"], row["lecturer_id"])
