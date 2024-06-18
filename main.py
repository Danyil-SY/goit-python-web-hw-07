import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Teacher, Group, Student, Subject, Grade

DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def create_teacher(name: str):
    teacher = Teacher(fullname=name)
    session.add(teacher)
    session.commit()


def list_teachers():
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(teacher.id, teacher.fullname)


def update_teacher(teacher_id: int, name: str):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher:
        teacher.fullname = name
        session.commit()


def delete_teacher(teacher_id: int):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher:
        session.delete(teacher)
        session.commit()


def create_group(name: str):
    group = Group(name=name)
    session.add(group)
    session.commit()


def list_groups():
    groups = session.query(Group).all()
    for group in groups:
        print(group.id, group.name)


def update_group(group_id: int, name: str):
    group = session.query(Group).filter(Group.id == group_id).first()
    if group:
        group.name = name
        session.commit()


def delete_group(group_id: int):
    group = session.query(Group).filter(Group.id == group_id).first()
    if group:
        session.delete(group)
        session.commit()


def create_student(fullname: str, group_id: int):
    student = Student(fullname=fullname, group_id=group_id)
    session.add(student)
    session.commit()


def list_students():
    students = session.query(Student).all()
    for student in students:
        print(student.id, student.fullname, student.group_id)


def update_student(student_id: int, fullname: str = None, group_id: int = None):
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        if fullname:
            student.fullname = fullname
        if group_id:
            student.group_id = group_id
        session.commit()


def delete_student(student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        session.delete(student)
        session.commit()


def create_subject(name: str, teacher_id: int):
    subject = Subject(name=name, teacher_id=teacher_id)
    session.add(subject)
    session.commit()


def list_subjects():
    subjects = session.query(Subject).all()
    for subject in subjects:
        print(subject.id, subject.name, subject.teacher_id)


def update_subject(subject_id: int, name: str = None, teacher_id: int = None):
    subject = session.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        if name:
            subject.name = name
        if teacher_id:
            subject.teacher_id = teacher_id
        session.commit()


def delete_subject(subject_id: int):
    subject = session.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        session.delete(subject)
        session.commit()


def main():
    parser = argparse.ArgumentParser(description="CRUD operations for the database")
    parser.add_argument(
        "-a",
        "--action",
        type=str,
        required=True,
        help="Action to perform: create, list, update, remove",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        required=True,
        help="Model to perform action on: Teacher, Group, Student, Subject",
    )
    parser.add_argument("--id", type=int, help="ID of the model")
    parser.add_argument("--name", type=str, help="Name of the model")
    parser.add_argument("--group_id", type=int, help="Group ID for student")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for subject")

    args = parser.parse_args()

    if args.model == "Teacher":
        if args.action == "create" and args.name:
            create_teacher(args.name)
        elif args.action == "list":
            list_teachers()
        elif args.action == "update" and args.id and args.name:
            update_teacher(args.id, args.name)
        elif args.action == "remove" and args.id:
            delete_teacher(args.id)

    elif args.model == "Group":
        if args.action == "create" and args.name:
            create_group(args.name)
        elif args.action == "list":
            list_groups()
        elif args.action == "update" and args.id and args.name:
            update_group(args.id, args.name)
        elif args.action == "remove" and args.id:
            delete_group(args.id)

    elif args.model == "Student":
        if args.action == "create" and args.name and args.group_id:
            create_student(args.name, args.group_id)
        elif args.action == "list":
            list_students()
        elif args.action == "update" and args.id:
            update_student(args.id, args.name, args.group_id)
        elif args.action == "remove" and args.id:
            delete_student(args.id)

    elif args.model == "Subject":
        if args.action == "create" and args.name and args.teacher_id:
            create_subject(args.name, args.teacher_id)
        elif args.action == "list":
            list_subjects()
        elif args.action == "update" and args.id:
            update_subject(args.id, args.name, args.teacher_id)
        elif args.action == "remove" and args.id:
            delete_subject(args.id)


if __name__ == "__main__":
    main()
