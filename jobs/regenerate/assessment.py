from database.seeders import assessments_seeder
from app.services import discord
from app.models import AssessmentRepository


def get_closure(symbol: str):
    """
    Delete old Assessment and create a new one for the symbol
    """

    def closure():
        try:
            # delete the old assessment
            AssessmentRepository().get_collection().delete_one(
                filter={"symbol": symbol}
            )

            # regenerate new assessment
            assessments_seeder.main(symbol)

            msg = f"Đã tạo lại nhận định cho mã **{symbol}**"
            discord.send(msg)
        except Exception as e:
            # Catch any type of exception and access its message
            print(f"An error occurred: {e}")

    return closure
