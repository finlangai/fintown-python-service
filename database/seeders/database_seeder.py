from . import (
    assessments_seeder,
    companies_seeder,
    dividends_seeder,
    events_seeder,
    formats_seeder,
    formulars_seeder,
    holders_seeder,
    metrics_seeder,
    news_seeder,
    statements_seeder,
    subsidiaries_seeder,
)


def main():
    """Bỏ comment để bơm dữ liệu cho bảng nhất định
    Lưu ý: Statement Seeder dựa vào dữ liệu profile trong Database chứ không dựa theo config
    """
    companies_seeder.main()
    dividends_seeder.main()
    events_seeder.main()
    holders_seeder.main()
    news_seeder.main()
    subsidiaries_seeder.main()

    statements_seeder.main()
    formats_seeder.main()

    formulars_seeder.main()
    metrics_seeder.main()
    assessments_seeder.main()


if __name__ == "__main__" or __name__ == "tasks":
    main()
