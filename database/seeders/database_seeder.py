from . import (
    companies_seeder,
    formulars_seeder,
    holders_seeder,
    dividends_seeder,
    statements_seeder,
    formats_seeder,
)


def main():
    """Bỏ comment để bơm dữ liệu cho bảng nhất định
    Lưu ý: Statement Seeder dựa vào dữ liệu profile trong Database chứ không dựa theo config
    """
    companies_seeder.main()
    holders_seeder.main()
    dividends_seeder.main()
    statements_seeder.main()
    formats_seeder.main()
    formulars_seeder.main()


if __name__ == "__main__" or __name__ == "tasks":
    main()
