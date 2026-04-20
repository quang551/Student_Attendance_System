from datetime import datetime

from models.attendance import Attendance, AttendanceStatus
from repositories.attendance_repo import AttendanceRepo


class AttendanceService:
    def __init__(self, attendance_repo=None):
        self.attendance_repo = attendance_repo or AttendanceRepo()

    def open_session(self, session_id):
        if not self.attendance_repo.get_session(session_id):
            return False, "Session not found!"
        self.attendance_repo.update_session_status(session_id, True)
        return True, "Session opened!"

    def close_session(self, session_id):
        if not self.attendance_repo.get_session(session_id):
            return False, "Session not found!"
        self.attendance_repo.update_session_status(session_id, False)
        return True, "Session closed!"

    def is_session_open(self, session_id):
        session = self.attendance_repo.get_session(session_id)
        return bool(session and session["is_open"])

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
