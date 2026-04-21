from models.course import Course
from repositories.db import get_connection


class CourseRepo:
    def add(self, course):
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO course (course_id, course_name, description)
            VALUES (?, ?, ?)
            """,
            (course.course_id, course.name, course.description),
        )
        conn.commit()
        conn.close()
        return course

    def get_all(self):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT course_id, course_name, description
            FROM course
            ORDER BY course_id
            """
        ).fetchall()
        conn.close()
        return [self._to_course(row) for row in rows]

    def find_by_id(self, course_id):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT course_id, course_name, description
            FROM course
            WHERE course_id = ?
            """,
            (course_id,),
        ).fetchone()
        conn.close()
        return self._to_course(row)

    def get_classes_using_course(self, course_id):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT class_id, class_name
            FROM class
            WHERE course_id = ?
            ORDER BY class_id
            """,
            (course_id,),
        ).fetchall()
        conn.close()
        return rows

    def delete(self, course_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course WHERE course_id = ?", (course_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def update(self, course_id, new_name=None, new_description=None):
        current = self.find_by_id(course_id)
        if not current:
            return False

        conn = get_connection()
        conn.execute(
            """
            UPDATE course
            SET course_name = ?, description = ?
            WHERE course_id = ?
            """,
            (
                new_name if new_name is not None else current.name,
                new_description if new_description is not None else current.description,
                course_id,
            ),
        )
        conn.commit()
        conn.close()
        return True

    def _to_course(self, row):
        if not row:
            return None
        return Course(row["course_id"], row["course_name"], row["description"])
