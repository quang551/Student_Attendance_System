from services.report_service import ReportService

class ReportCLI:
    def __init__(self):
        self.service = ReportService()

    def run(self):
        while True:
            print("\n=== REPORT ===")
            print("1. Theo lớp")
            print("2. Theo sinh viên")
            print("0. Thoát")

            c = input("Chọn: ")

            if c == "1":
                cid = input("Nhập class_id: ")
                r = self.service.report_by_class(cid)
                print(r)

            elif c == "2":
                sid = input("Nhập student_id: ")
                r = self.service.report_by_student(sid)
                print(r)

            elif c == "0":
                break