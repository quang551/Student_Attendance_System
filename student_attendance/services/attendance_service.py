from datetime import datetime
from repositories.attendance_repo import *


def open_session(session_id):
    update_session_status(session_id, "1")


def close_session(session_id):
    update_session_status(session_id, "0")


def is_session_open(session_id):
    session = get_session(session_id)
    if session:
        return session[4] == "1"   # is_open
    return False

def mark_attendance(attendance_id, session_id, student_id, status):

    # ❗ 1. check session mở
    if not is_session_open(session_id):
        print("❌ Session chưa mở")
        return

    # ❗ 2. lấy class_id từ session
    class_id = get_class_id_by_session(session_id)

    if not class_id:
        print("❌ Session không tồn tại")
        return

    # ❗ 3. check student có trong class không
    if not is_student_in_class(student_id, class_id):
        print("❌ Student không thuộc lớp này")
        return

    # ❗ 4. xử lý điểm danh
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    existing = get_attendance(session_id, student_id)

    if existing:
        update_attendance(session_id, student_id, status, now)
    else:
        insert_attendance(attendance_id, session_id, student_id, status, now)


def view_attendance_by_session(session_id):
    return get_attendance_by_session(session_id)


def view_attendance_by_student(student_id):
    return get_attendance_by_student(student_id)