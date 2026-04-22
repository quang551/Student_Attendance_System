from datetime import datetime

from student_attendance.models.attendance import Attendance, AttendanceStatus
from student_attendance.repositories.attendance_repo import AttendanceRepo
from student_attendance.repositories.session_repo import SessionRepo


class AttendanceService:
    def __init__(self, attendance_repo=None, session_repo=None):
        self.attendance_repo = attendance_repo or AttendanceRepo()
        self.session_repo = session_repo or SessionRepo()

    def open_session(self, session_id):
        session = self.session_repo.find_by_id(session_id)
        if not session:
            return False, "Session not found!"

        if session.is_open:
            return False, "Session is already open!"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session_repo.update(
            session_id,
            start_time=now,
            is_open=True,
        )
        return True, f"Session opened at {now}"

    def close_session(self, session_id):
        session = self.session_repo.find_by_id(session_id)
        if not session:
            return False, "Session not found!"

        if not session.is_open:
            return False, "Session is already closed!"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session_repo.update(
            session_id,
            end_time=now,
            is_open=False,
        )
        return True, f"Session closed at {now}"

    def is_session_open(self, session_id):
        session = self.attendance_repo.get_session(session_id)
        if not session:
            return False

        raw_is_open = session["is_open"]
        try:
            return bool(int(raw_is_open))
        except (TypeError, ValueError):
            return False

    def get_class_id_by_session(self, session_id):
        return self.attendance_repo.get_class_id_by_session(session_id)

    def mark_attendance(self, attendance_id, session_id, student_id, status):
        if int(status) not in {int(item) for item in AttendanceStatus}:
            return False, "Invalid attendance status"

        if not self.is_session_open(session_id):
            return False, "Session is not open"

        class_id = self.attendance_repo.get_class_id_by_session(session_id)
        if not class_id:
            return False, "Session not found"

        if not self.attendance_repo.is_student_in_class(student_id, class_id):
            return False, "Student is not enrolled in this class"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existing = self.attendance_repo.get_attendance(session_id, student_id)

        if existing:
            self.attendance_repo.update_attendance(session_id, student_id, status, now)
            return True, "Attendance updated"

        attendance = Attendance(attendance_id, session_id, student_id, int(status), now)
        self.attendance_repo.insert_attendance(attendance)
        return True, "Attendance recorded"

    def view_attendance_by_session(self, session_id):
        return self.attendance_repo.get_attendance_by_session(session_id)

    def view_attendance_by_student(self, student_id):
        return self.attendance_repo.get_attendance_by_student(student_id)
