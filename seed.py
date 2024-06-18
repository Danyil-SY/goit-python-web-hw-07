import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade


fake = Faker()

DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def seed_database():
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    subjects = [
        Subject(name=f"Subject {i+1}", teacher=random.choice(teachers))
        for i in range(8)
    ]
    session.add_all(subjects)
    session.commit()

    students = [
        Student(fullname=fake.name(), group=random.choice(groups)) for _ in range(50)
    ]
    session.add_all(students)
    session.commit()

    for student in students:
        for subject in subjects:
            for _ in range(20):
                grade = Grade(
                    grade=random.uniform(1, 10),
                    date_received=fake.date_between(start_date="-1y", end_date="today"),
                    student=student,
                    subject=subject,
                )
                session.add(grade)
    session.commit()


if __name__ == "__main__":
    seed_database()
