from models.session import Session
from repositories.db import get_connection


class SessionRepo:
    def add(self, session):
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO session (session_id, class_id, start_time, end_time, is_open)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session.session_id, session.class_id, session.start_time, session.end_time, int(session.is_open)),
        )
        conn.commit()
        conn.close()
        return session

    def get_all(self):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT session_id, class_id, start_time, end_time, is_open
            FROM session
            ORDER BY start_time
            """
        ).fetchall()
        conn.close()
        return [self._to_session(row) for row in rows]

    def find_by_id(self, session_id):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT session_id, class_id, start_time, end_time, is_open
            FROM session
            WHERE session_id = ?
            """,
            (session_id,),
        ).fetchone()
        conn.close()
        return self._to_session(row)

    def list_by_class(self, class_id):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT session_id, class_id, start_time, end_time, is_open
            FROM session
            WHERE class_id = ?
            ORDER BY start_time
            """,
            (class_id,),
        ).fetchall()
        conn.close()
        return [self._to_session(row) for row in rows]

    def delete(self, session_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM session WHERE session_id = ?", (session_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def update(self, session_id, start_time=None, end_time=None, is_open=None):
        current = self.find_by_id(session_id)
        if not current:
            return False

        conn = get_connection()
        conn.execute(
            """
            UPDATE session
            SET start_time = ?, end_time = ?, is_open = ?
            WHERE session_id = ?
            """,
            (
                start_time if start_time is not None else current.start_time,
                end_time if end_time is not None else current.end_time,
                int(is_open) if is_open is not None else int(current.is_open),
                session_id,
            ),
        )
        conn.commit()
        conn.close()
        return True

    def _to_session(self, row):
        if not row:
            return None
        return Session(row["session_id"], row["class_id"], row["start_time"], row["end_time"], bool(row["is_open"]))
