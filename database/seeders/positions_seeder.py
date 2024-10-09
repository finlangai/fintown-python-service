from app.utils import print_green_bold
from app.models import PositionRepository, Position


def main():
    print_green_bold("=== SEEDING OFFICERS")

    position_list = [
        {"id": 1, "name": "Chủ tịch HĐQT"},
        {"id": 2, "name": "Tổng giám đốc"},
        {"id": 3, "name": "Thành viên HĐQT"},
        {"id": 4, "name": "Trưởng ban kiểm soát"},
        {"id": 5, "name": "Thành viên ban kiểm soát"},
        {"id": 6, "name": "Phó tổng giám đốc"},
        {"id": 7, "name": "Giám đốc điều hành"},
        {"id": 8, "name": "Phó giám đốc điều hành"},
        {"id": 9, "name": "Phó Chủ tịch HĐQT"},
        {"id": 10, "name": "Giám đốc chi nhánh"},
        {"id": 11, "name": "Kế toán trưởng"},
        {"id": 12, "name": "Đại diện công bố thông tin"},
        {"id": 13, "name": "Giám đốc tài chính"},
        {"id": 14, "name": "Giám đốc kinh doanh"},
        {"id": 15, "name": "Giám đốc chất lượng"},
        {"id": 16, "name": "Giám đốc kỹ thuật"},
        {"id": 17, "name": "Phó giám đốc kỹ thuật"},
        {"id": 19, "name": "Chủ tịch Ban đại diện quỹ"},
        {"id": 20, "name": "Giám đốc nhân sự"},
        {"id": 21, "name": "Phó giám đốc sản xuất"},
        {"id": 22, "name": "Phó giám đốc kinh doanh"},
        {"id": 23, "name": "Phó tổng giám đốc tài chính"},
        {"id": 24, "name": "Phó tổng giám đốc kinh doanh"},
        {"id": 26, "name": "Phó ban kiểm soát"},
        {"id": 27, "name": "Giám đốc sản xuất"},
        {"id": 28, "name": "Giám đốc thu mua"},
        {"id": 29, "name": "Giám đốc dự án"},
        {"id": 30, "name": "Chưa xác định"},
        {"id": 31, "name": "Trưởng ban kiểm toán nội bộ"},
        {"id": 34, "name": "Giám đốc đầu tư"},
        {"id": 39, "name": "Phó giám đốc chi nhánh"},
        {"id": 41, "name": "Thành viên ban kiểm toán nội bộ"},
        {"id": 42, "name": "Người phụ trách quản trị công ty"},
        {"id": 43, "name": "Giám đốc tiếp thị"},
        {"id": 44, "name": "Giám đốc bộ phận"},
        {"id": 45, "name": "Chủ tịch Ủy ban kiểm toán"},
        {"id": 46, "name": "Phó chủ tịch Ủy ban kiểm toán"},
        {"id": 47, "name": "Thành viên Ủy ban kiểm toán"},
        {"id": 48, "name": "Thư ký HĐQT"},
        {"id": 49, "name": "Phó tổng giám đốc kế hoạch"},
    ]

    model_accumulator: list[Position] = []
    for item in position_list:
        model = Position(**item)
        model_accumulator.append(model)
    PositionRepository().save_many(model_accumulator)
    print_green_bold(f"=== {len(position_list)} position seeded")


if __name__ == "__main__" or __name__ == "tasks":
    main()
