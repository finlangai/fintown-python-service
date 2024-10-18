from database.seeders import stash_stats_seeder
from app.services import discord


def get_closure():
    """
    Update the stats on stash collection for all symbol
    """

    def closure():
        try:
            # regenerate new assessment
            amount = stash_stats_seeder.main()

            msg = f"Đã cập nhật chỉ số hằng ngày cho **{amount}** mã"
            discord.send(msg)
        except Exception as e:
            # Catch any type of exception and access its message
            print(f"An error occurred: {e}")

    return closure
