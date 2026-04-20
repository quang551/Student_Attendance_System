from repositories.db import get_connection
from models.user import User


class UserRepo:
    def create(self, user, role_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (user_id, user_name, full_name, password, email, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user.user_id,
            user.username,
            user.full_name,
            user.password,
            user.email,
            user.role,
        ))

        self._upsert_role_table(cursor, user.user_id, user.role, role_id)
        conn.commit()
        conn.close()
        return user

    def get_by_username(self, username):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, user_name, full_name, email, role, password
            FROM users
            WHERE user_name = ?
        """, (username,))
        row = cursor.fetchone()
        conn.close()
        return self._to_user(row)

    def get_by_id(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, user_name, full_name, email, role, password
            FROM users
            WHERE user_id = ?
        """, (user_id,))
        row = cursor.fetchone()
        conn.close()
        return self._to_user(row)

    def list_all(self, role=None):
        conn = get_connection()
        cursor = conn.cursor()

        if role:
            cursor.execute("""
                SELECT user_id, user_name, full_name, email, role, password
                FROM users
                WHERE role = ?
                ORDER BY user_name
            """, (role,))
        else:
            cursor.execute("""
                SELECT user_id, user_name, full_name, email, role, password
                FROM users
                ORDER BY user_name
            """)

        rows = cursor.fetchall()
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

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET user_name = ?, full_name = ?, password = ?, email = ?, role = ?
            WHERE user_id = ?
        """, (
            next_username,
            next_full_name,
            next_password,
            next_email,
            next_role,
            user_id,
        ))

        self._upsert_role_table(cursor, user_id, next_role)
        conn.commit()
        conn.close()
        return self.get_by_id(user_id)

    def delete(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM lecturer WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM student WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def authenticate(self, username, password_hash):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, user_name, full_name, email, role, password
            FROM users
            WHERE user_name = ? AND password = ?
        """, (username, password_hash))
        row = cursor.fetchone()
        conn.close()
        return self._to_user(row)

    def ensure_role_user(self, role_id, username, full_name, role, password_hash):
        existing = self.get_role_user(role, role_id)
        if existing:
            return existing

        user = User(
            user_id=f"U_{role_id}",
            username=username,
            full_name=full_name,
            email=f"{username}@example.com",
            role=role,
            password=password_hash,
        )
        self.create(user, role_id=role_id)
        return user

    def get_role_user(self, role, role_id):
        table = {"admin": "admin", "lecturer": "lecturer", "student": "student"}[role]
        pk = {"admin": "admin_id", "lecturer": "lecturer_id", "student": "student_id"}[role]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT u.user_id, u.user_name, u.full_name, u.email, u.role, u.password
            FROM {table} r
            JOIN users u ON u.user_id = r.user_id
            WHERE r.{pk} = ?
        """, (role_id,))
        row = cursor.fetchone()
        conn.close()
        return self._to_user(row)

    def _to_user(self, row):
        if not row:
            return None
        return User(
            user_id=row[0],
            username=row[1],
            full_name=row[2],
            email=row[3],
            role=row[4],
            password=row[5],
        )

    def _upsert_role_table(self, cursor, user_id, role, role_id=None):
        cursor.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM lecturer WHERE user_id = ?", (user_id,))
        cursor
