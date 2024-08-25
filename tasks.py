from invoke import task


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

        getattr(seeders, f"{name}_seeder").main()
        print(f"{name} seeded")

    except Exception as e:
        e.with_traceback(e.__traceback__)
        print(e)
        print("Hell nah")
