from app.models import StatementFormat, FieldInfo, ICBRange
from app.enums import StatementType
from app.services import get_financial_statement
from app.utils import model_mapper, natural_to_snake, json_camel_to_snake
from core.mongodb import insert_one


def main():
    print("inw")
    # Format theo thứ tự bên dưới cùng mã chứng khoán sẽ sử dụng
    # Chung: hpg
    # Ngân Hàng: vcb
    # Chứng Khoán: aps
    # Bảo hiểm: bvh

    symbol_list = ["hpg", "vcb", "vix", "bvh"]

    raw_icb_ranges = [
        [["0001", "7577"], ["8600", "8779"], ["9000", "9578"]],
        [["8300", "8355"]],
        [["8500", "8581"]],
        [["8780", "8781"]],
    ]

    for symbol, icb_ranges in zip(symbol_list, raw_icb_ranges):
        structures = dict()
        for type in StatementType:
            # Tạo hàm closure
            def get_statement(type: StatementType):
                return get_financial_statement(
                    symbol=symbol, type=type, limit=1, quarter=0
                )

            structures[type.name.lower()] = [
                model_mapper(
                    model=FieldInfo,
                    data=json_camel_to_snake(field),
                    shifted_fields={
                        "snake_case": natural_to_snake(text=field.get("name"))
                    },
                )
                for field in get_statement(type=type)
            ]
        format = StatementFormat(
            structures=structures,
            icb_ranges=[ICBRange(start=range[0], end=range[1]) for range in icb_ranges],
        )
        insert_one(
            collection_name=StatementFormat.get_collection_name(),
            document=format.model_dump(),
        )


if __name__ == "__main__" or __name__ == "tasks":
    main()
