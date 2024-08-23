from invoke import task


@task
def dev(c):
    c.run("fastapi dev server.py")


@task
def inw(c):
    c.run("pymon inw.py")


@task
def seed(c, name):
    # c.run(f"python database/seeders/{name}_seeder.py")
    try:
        with open(f"database/seeders/{name}_seeder.py") as pycode:
            exec(pycode.read())
        print(f"{name} seeded")

    except:
        print("Hell nah")
