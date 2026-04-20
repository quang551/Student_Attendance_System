class ReportService:
    def __init__(self):
        # dữ liệu giả
        self.data = [
            {"student_id": "S1", "class_id": "C1", "status": "present"},
            {"student_id": "S1", "class_id": "C1", "status": "absent"},
            {"student_id": "S2", "class_id": "C1", "status": "present"},
            {"student_id": "S2", "class_id": "C1", "status": "present"},
        ]

    def report_by_class(self, class_id):
        records = [r for r in self.data if r["class_id"] == class_id]

        total = len(records)
        present = sum(1 for r in records if r["status"] == "present")
        absent = total - present
        rate = (present / total * 100) if total else 0

        return {
            "total": total,
            "present": present,
            "absent": absent,
            "rate": round(rate, 2)
        }

    def report_by_student(self, student_id):
        records = [r for r in self.data if r["student_id"] == student_id]

        total = len(records)
        present = sum(1 for r in records if r["status"] == "present")
        absent = total - present
        rate = (present / total * 100) if total else 0

        return {
            "total": total,
            "present": present,
            "absent": absent,
            "rate": round(rate, 2)
        }