from database.seeders import assessments_seeder


def get_closure(symbol: str):
    def closure():
        try:
            assessments_seeder.main(symbol)
        except Exception as e:
            # Catch any type of exception and access its message
            print(f"An error occurred: {e}")

    return closure
