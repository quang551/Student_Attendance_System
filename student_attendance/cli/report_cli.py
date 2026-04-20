def report_menu(service):
    while True:
        print("\n=== REPORT ===")
        print("1. Theo lớp")
        print("2. Theo sinh viên")
        print("0. Quay lại")

        choice = input("Chọn: ").strip()
        if choice == "1":
            class_id = input("Nhập class_id: ").strip()
            _print_report(service.report_by_class(class_id))
        elif choice == "2":
            student_id = input("Nhập student_id: ").strip()
            _print_report(service.report_by_student(student_id))
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ.")


def _print_report(report):
    print(f"Tổng số: {report['total']}")
    print(f"Có mặt: {report['present']}")
    print(f"Vắng: {report['absent']}")
    print(f"Muộn: {report['late']}")
    print(f"Tỷ lệ có mặt: {report['rate']}%")
