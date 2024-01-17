import random

from app.db.db_manager import DBManager
from app.models import Base, User, Breed, Food, Pet, Reminder
from faker import Faker

fake = Faker()


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
        password='12345',
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


def create_fake_reminders(session):
    med_reminder = Reminder(user_id=1, title='Medication', start='2023-12-10', end='2023-12-10')
    play_reminder = Reminder(user_id=1, title='play', start='2023-12-05', end='2023-12-05')
    exercise_reminder = Reminder(user_id=2, title='exercise', start='2023-12-21', end='2023-12-23')
    session.add(med_reminder)
    session.add(play_reminder)
    session.add(exercise_reminder)
    session.commit()


def create_fake_pets(session):
    boo = Pet(user_id=1, breed_id=2, name='Boo', age=11, weight='25', birthday='2012-10-05')
    session.add(boo)
    miles = Pet(user_id=1, breed_id=1, name='Miles', age=8, weight='75', birthday='2015-03-15')
    session.add(miles)
    flare = Pet(user_id=1, breed_id=1, name='Flare', age=7, weight='67', birthday='2016-08-21')
    session.add(flare)
    session.commit()


def create_fake_foods(session):
    orijen_senior_dry = Food(type='dry', name='Orijen: Senior', ingredients=None, crude_protein=38, crude_fat=15, crude_fiber=8, moisture=12, dietary_starch=17, epa=0.2, calcium=1.3, phosphorus=0.9, vitamin_e=750, omega_6=3, omega_3=0.8, glucosamine=600, microorganisms=1000000)
    session.add(orijen_senior_dry)
    purina_pro_plan = Food(type='dry', name='Purina Pro Plan Complete Essentials Adult Dry Dog Food - High Protein, Probiotics, Beef & Rice', ingredients='Beef, Rice, Whole Grain Wheat, Corn Gluten Meal, Poultry By-product Meal (Source Of Glucosamine), Soybean Meal, Whole Grain Corn, Beef Fat Preserved With Mixed-tocopherols, Dried Egg Product, Dried Beet Pulp, Fish Meal (Source Of Glucosamine), Natural Flavor, Glycerin, Calcium Carbonate, Wheat Bran, Mono And Dicalcium Phosphate, Soybean Oil, Salt, Potassium Chloride, Vitamins [Vitamin E Supplement, Niacin (Vitamin B-3), Vitamin A Supplement, Calcium Pantothenate (Vitamin B-5), Thiamine Mononitrate (Vitamin B-1), Vitamin B-12 Supplement, Riboflavin Supplement (Vitamin B-2), Pyridoxine Hydrochloride (Vitamin B-6), Folic Acid (Vitamin B-9), Vitamin D-3 Supplement, Menadione Sodium Bisulfite Complex (Vitamin K), Biotin (Vitamin B-7)], Minerals [Zinc Proteinate, Manganese Proteinate, Ferrous Sulfate, Copper Proteinate, Calcium Iodate, Sodium Selenite], Choline Chloride, L-ascorbyl-2-polyphosphate (Vitamin C), Dried Bacillus Coagulans Fermentation Product, Garlic Oil. P446919', crude_protein=26, crude_fat=16, crude_fiber=3, moisture=12, dietary_starch=None, epa=None, calcium=1, phosphorus=0.8, vitamin_e=460, omega_6=1.5, omega_3=None, glucosamine=400, microorganisms=600000000)
    session.add(purina_pro_plan)
    session.commit()


def create_fake_breeds(session):
    husky = Breed(name='Husky', suggested_supplements=None, suggested_exercise="walks")
    session.add(husky)
    american_eskimo = Breed(name='American Eskimo', suggested_supplements=None, suggested_exercise="running")
    session.add(american_eskimo)
    bulldog = Breed(name='Bulldog', suggested_supplements=None, suggested_exercise="swimming")
    session.add(bulldog)
    session.commit()


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

    #fake breeds
    print("{0}. creating some fake breeds...".format(step))
    breeds = create_fake_breeds(session)
    step += 1

    #fake foods
    print("{0}. creating some fake foods...".format(step))
    foods = create_fake_foods(session)
    step += 1

    #fake pets
    print("{0}. creating some fake pets...".format(step))
    pets = create_fake_pets(session)
    step += 1

    #fake reminders
    print("{0}. creating some fake reminders...".format(step))
    reminders = create_fake_reminders(session)


    # cleanup
    db_manager.cleanup()


# if __name__ == "__main__":
#     generate_data()
