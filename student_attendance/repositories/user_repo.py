from student_attendance.repositories.db import get_connection
from student_attendance.models.user import Admin, Lecturer, Student, User


class UserRepo:
    ROLE_TABLE = {
        "admin": ("admin", "admin_id", "A"),
        "lecturer": ("lecturer", "lecturer_id", "L"),
        "student": ("student", "student_id", "S"),
    }

    def create(self, user, role_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (user_id, user_name, full_name, password, email, role)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user.user_id,
                    user.username,
                    user.full_name,
                    user.password,
                    user.email,
                    user.role,
                ),
            )
            self._upsert_role_table(cursor, user.user_id, user.role, role_id)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

        return self.get_by_id(user.user_id)

    def get_by_username(self, username):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT user_id, user_name, full_name, email, role, password
            FROM users
            WHERE user_name = ?
            """,
            (username,),
        ).fetchone()
        conn.close()
        return self._to_user(row)

    def get_by_id(self, user_id):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT user_id, user_name, full_name, email, role, password
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()
        conn.close()
        return self._to_user(row)

    def list_all(self, role=None):
        conn = get_connection()
        if role:
            rows = conn.execute(
                """
                SELECT user_id, user_name, full_name, email, role, password
                FROM users
                WHERE role = ?
                ORDER BY user_name
                """,
                (role,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT user_id, user_name, full_name, email, role, password
                FROM users
                ORDER BY user_name
                """
            ).fetchall()
        conn.close()
        return [self._to_user(row) for row in rows]

    def update(self, user_id, **fields):
        current = self.get_by_id(user_id)
        if not current:
            return None

        next_username = fields.get("username", current.username)
        next_full_name = fields.get("full_name", current.full_name)
        next_email = fields.get("email", current.email)
        next_password = fields.get("password", current.password)
        next_role = fields.get("role", current.role)
        next_role_id = fields.get("role_id")

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE users
                SET user_name = ?, full_name = ?, password = ?, email = ?, role = ?
                WHERE user_id = ?
                """,
                (
                    next_username,
                    next_full_name,
                    next_password,
                    next_email,
                    next_role,
                    user_id,
                ),
            )
            self._upsert_role_table(cursor, user_id, next_role, next_role_id)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

        return self.get_by_id(user_id)

    def delete(self, user_id):
        current = self.get_by_id(user_id)
        if not current:
            return False

        role = current.role
        role_id = None
        if role in self.ROLE_TABLE:
            role_id = self._get_role_id_by_user_id(role, user_id)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            if role == "lecturer" and role_id:
                cursor.execute(
                    """
                    UPDATE class
                    SET lecturer_id = NULL
                    WHERE lecturer_id = ?
                    """,
                    (role_id,),
                )

            elif role == "student" and role_id:
                cursor.execute(
                    """
                    DELETE FROM attendance
                    WHERE student_id = ?
                    """,
                    (role_id,),
                )
                cursor.execute(
                    """
                    DELETE FROM class_student
                    WHERE student_id = ?
                    """,
                    (role_id,),
                )

            cursor.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM lecturer WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM student WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def authenticate(self, username, password_hash):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT user_id, user_name, full_name, email, role, password
            FROM users
            WHERE user_name = ? AND password = ?
            """,
            (username, password_hash),
        ).fetchone()
        conn.close()
        return self._to_user(row)

    def get_role_user(self, role, role_id):
        table, pk, _ = self.ROLE_TABLE[role]
        conn = get_connection()
        row = conn.execute(
            f"""
            SELECT u.user_id, u.user_name, u.full_name, u.email, u.role, u.password
            FROM {table} r
            JOIN users u ON u.user_id = r.user_id
            WHERE r.{pk} = ?
            """,
            (role_id,),
        ).fetchone()
        conn.close()
        return self._to_user(row, role_id)

    def _get_role_id_by_user_id(self, role, user_id):
        table, pk, _ = self.ROLE_TABLE[role]
        conn = get_connection()
        row = conn.execute(
            f"SELECT {pk} FROM {table} WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        conn.close()
        return row[pk] if row else None

    def _to_user(self, row, role_id=None):
        if not row:
            return None

        role = row["role"]
        resolved_role_id = role_id or self._get_role_id_by_user_id(role, row["user_id"])

        kwargs = {
            "user_id": row["user_id"],
            "username": row["user_name"],
            "full_name": row["full_name"],
            "email": row["email"],
            "role": role,
            "password": row["password"],
        }

        if role == "admin":
            return Admin(admin_id=resolved_role_id, **kwargs)
        if role == "lecturer":
            return Lecturer(lecturer_id=resolved_role_id, **kwargs)
        if role == "student":
            return Student(student_id=resolved_role_id, **kwargs)
        return User(**kwargs)

    def _upsert_role_table(self, cursor, user_id, role, role_id=None):
        cursor.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM lecturer WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM student WHERE user_id = ?", (user_id,))

        table, pk, prefix = self.ROLE_TABLE[role]
        resolved_role_id = role_id or f"{prefix}{user_id}"
        cursor.execute(
            f"INSERT INTO {table} ({pk}, user_id) VALUES (?, ?)",
            (resolved_role_id, user_id),
        )
