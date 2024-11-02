from database.seeders import update_quotes_seeder
from app.services import discord


def get_closure():
    """
    Get the newest quotes for stock symbols
    """

    def closure():
        try:
            # regenerate new assessment
            amount = update_quotes_seeder.main()

            msg = f"Đã cập nhật giá cổ phiếu cho **{amount}** mã ヾ(•ω•`)o"
            discord.send(msg)
        except Exception as e:
            # Catch any type of exception and access its message
            print(f"An error occurred: {e}")

    return closure
