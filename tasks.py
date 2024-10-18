from invoke import task
import time
from app.utils import print_green_bold, print_pink_bold
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")


@task
def dev(c):
    c.run("fastapi dev server.py --port 8006")


@task
def inw(c):
    c.run("python inw.py")


@task
def seed(c, name):
    from database import seeders

    start_time = time.time()

    getattr(seeders, f"{name}_seeder").main()
    print_green_bold(
        f"{name} seeder done in {round(time.time() - start_time, 2)} seconds （＾∀＾●）ﾉｼ"
    )


@task
def recal(c):
    from core import mongodb

    # delete formulars
    print_pink_bold("=== deleting formulars")
    mongodb.delete_many("formular_library", {})
    # delete metrics
    print_pink_bold("=== deleting metrics")
    mongodb.delete_many("metric_records", {})

    from database.seeders import formulars_seeder, metrics_seeder

    print_green_bold("=== seeding formulars")
    formulars_seeder.main()
    print_green_bold("=== seeding metrics")
    metrics_seeder.main()
