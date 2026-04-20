from dataclasses import dataclass
from enum import IntEnum


class AttendanceStatus(IntEnum):
    PRESENT = 1
    ABSENT = 2
    LATE = 3


@dataclass(slots=True)
class Attendance:
    attendance_id: str
    session_id: str
    student_id: str
    status: int
    recorded_at: str

    def mark_present(self):
        self.status = AttendanceStatus.PRESENT

    def mark_absent(self):
        self.status = AttendanceStatus.ABSENT

    def mark_late(self):
        self.status = AttendanceStatus.LATE

    def __str__(self):
        return (
            f"[{self.attendance_id}] Student: {self.student_id} | Session: {self.session_id} "
            f"| Status: {self.status} | Time: {self.recorded_at}"
        )