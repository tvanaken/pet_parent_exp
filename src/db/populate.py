import random

from app.db.db_manager import DBManager
from app.models import Base, Task, User, Breed
from faker import Faker

fake = Faker()

tasks = [
    ["Dishes", "Do the dishes"],
    ["Sweep", "Sweep the floor"],
    ["Mow", "Mow the lawn"],
    ["Trash", "Take out the trash"],
    ["Groceries", "Buy groceries"],
    ["Exercise", "Do some jumping jax"],
    ["Homework", "Do SWE lab"],
]


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)


def create_user():
    profile = fake.simple_profile()
    tokens = profile["name"].split(" ")
    first_name = tokens.pop(0)
    last_name = " ".join(tokens)
    username = "{0}_{1}".format(first_name, last_name.replace(" ", "_")).lower()
    provider = profile["mail"].split("@")[1]
    email = "{0}@{1}".format(username, provider)
    user = User(
        email=email,
        hashed_password='12345',
        username = username
    )
    return user


def create_fake_users(session, n=5):
    users = []
    for _ in range(n):
        user = create_user()
        users.append(user)
        session.add(user)
    session.commit()
    return users


def create_fake_tasks(session, users, n=25):
    for _ in range(n):
        user = random.choice(users)
        task = create_task(user)
        session.add(task)
    session.commit()




def create_fake_breeds(session):
    husky = Breed(name='Husky', suggested_supplements=None, suggested_excercise="walks")
    session.add(husky)
    american_eskimo = Breed(name='American Eskimo', suggested_supplements=None, suggested_excercise="running")
    session.add(american_eskimo)
    bulldog = Breed(name='Bulldog', suggested_supplements=None, suggested_excercise="swimming")
    session.add(bulldog)
    session.commit()


def create_task(user):
    dummy_task = random.choice(tasks)
    task = Task(name=dummy_task[0], description=dummy_task[1], done=False, user=user)
    return task


def trigger_fastapi_reload():
    # Sneaky trick: triggering a hot reload, which releases
    # database sessions and allows database to be rebuilt:
    import subprocess

    subprocess.call(["touch", "server.py"])


def generate_data():
    print("\n1. Using touch command to trigger server reload...")
    trigger_fastapi_reload()

    print("\n2. Rebuilding database...")
    db_manager = DBManager()
    engine = db_manager.get_engine()
    session = db_manager.get_session()
    print(session)

    # drop all tables:
    step = 1
    print("{0}. Dropping all tables...".format(step))
    drop_tables(engine)
    step += 1

    # create all tables:
    print("{0}. creating DB tables (if they don't already exist)...".format(step))
    create_tables(engine)
    step += 1

    # fake users:
    print("{0}. creating some fake users...".format(step))
    users = create_fake_users(session, 5)
    step += 1

    # fake tasks:
    create_fake_tasks(session, users, n=25)
    print("{0}. creating some fake tasks...".format(step))
    step += 1

    #fake breeds
    create_fake_breeds(session)
    print("{0}. creating some fake breeds...".format(step))

    # cleanup
    db_manager.cleanup()


if __name__ == "__main__":
    generate_data()
