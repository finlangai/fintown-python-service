from invoke import task
import time
from app.utils import print_green_bold
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")


@task
def dev(c):
    c.run("fastapi dev server.py")


@task
def inw(c):
    c.run("python inw.py")


@task
def seed(c, name):
    try:
        from database import seeders

        start_time = time.time()

        getattr(seeders, f"{name}_seeder").main()
        print_green_bold(
            f"{name} seeded in {round(time.time() - start_time, 2)} seconds （＾∀＾●）ﾉｼ"
        )

    except Exception as e:
        # e.with_traceback(e.__traceback__)
        e.with_traceback()
        print(e)
        print("Hell nah")
