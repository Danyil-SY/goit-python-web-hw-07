from sqlalchemy import create_engine, cast, Numeric, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

DATABASE_URL: str = (
    "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def select_1() -> list[tuple[str, float]]:
    """Find 5 students with the highest average grade across all subjects."""
    result = (
        session.query(
            Student.fullname,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("average_grade"),
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(5)
        .all()
    )
    return result


def select_2(subject_id: int) -> tuple[str, float]:
    """Find the student with the highest average grade in a specific subject."""
    result = (
        session.query(
            Student.fullname,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("average_grade"),
        )
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .first()
    )
    return result


def select_3(subject_id: int) -> list[tuple[str, float]]:
    """Find the average grade in groups for a specific subject."""
    result = (
        session.query(
            Group.name,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("average_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Group, Student.group_id == Group.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.name)
        .all()
    )
    return result


def select_4() -> float:
    """Find the average grade across all grades in the database."""
    result = session.query(func.round(cast(func.avg(Grade.grade), Numeric), 2)).scalar()
    return result


def select_5(teacher_id: int) -> list[str]:
    """Find the courses taught by a specific teacher."""
    result = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
    return [row[0] for row in result]


def select_6(group_id: int) -> list[str]:
    """Find the list of students in a specific group."""
    result = session.query(Student.fullname).filter(Student.group_id == group_id).all()
    return [row[0] for row in result]


def select_7(group_id: int, subject_id: int) -> list[tuple[str, int]]:
    """Find the grades of students in a specific group for a specific subject."""
    result = (
        session.query(Student.fullname, Grade.grade)
        .select_from(Student)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    return result


def select_8(teacher_id: int) -> float:
    """Find the average grade given by a specific teacher across their subjects."""
    result = (
        session.query(
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("average_grade")
        )
        .select_from(Grade)
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    return result


def select_9(student_id: int) -> list[str]:
    """Find the list of courses attended by a specific student."""
    result = (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    return [row[0] for row in result]


def select_10(student_id: int, teacher_id: int) -> list[str]:
    """Find the list of courses taught to a specific student by a specific teacher."""
    result = (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    return [row[0] for row in result]


def select_11(teacher_id: int, student_id: int) -> float:
    """Find the average grade given by a specific teacher to a specific student."""
    result = (
        session.query(func.round(cast(func.avg(Grade.grade), Numeric), 2))
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.id == teacher_id, Grade.student_id == student_id)
        .scalar()
    )
    session.close()
    return result


def select_12(group_id: int, subject_id: int) -> list[tuple[str, int]]:
    """Find the grades of students in a specific group for a specific subject on the last session."""
    subquery = (
        session.query(func.max(Grade.date_received).label("max_date"))
        .join(Student)
        .join(Group)
        .filter(Group.id == group_id, Grade.subject_id == subject_id)
        .group_by(Student.id)
        .subquery()
    )

    result = (
        session.query(Student.fullname, Grade.grade)
        .select_from(Grade)
        .join(subquery, Grade.date_received == subquery.c.max_date)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(Group.id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    return result


if __name__ == "__main__":
    subject_id = 1
    teacher_id = 1
    group_id = 1
    student_id = 1

    print("5 students with the highest average grade across all subjects:")
    print(select_1())

    print(f"Student with the highest average grade in subject {subject_id}:")
    print(select_2(subject_id))

    print(f"Average grade in groups for subject {subject_id}:")
    print(select_3(subject_id))

    print("Average grade across all grades:")
    print(select_4())

    print(f"Courses taught by teacher {teacher_id}:")
    print(select_5(teacher_id))

    print(f"List of students in group {group_id}:")
    print(select_6(group_id))

    print(f"Grades of students in group {group_id} for subject {subject_id}:")
    print(select_7(group_id, subject_id))

    print(f"Average grade given by teacher {teacher_id}:")
    print(select_8(teacher_id))

    print(f"List of courses attended by student {student_id}:")
    print(select_9(student_id))

    print(f"List of courses taught to student {student_id} by teacher {teacher_id}:")
    print(select_10(student_id, teacher_id))

    print(f"Average grade given by teacher {teacher_id} to student {student_id}:")
    print(select_11(teacher_id, student_id))

    print(
        f"Grades of students in group {group_id} for subject {subject_id} on the last session:"
    )
    print(select_12(group_id, subject_id))

    session.close()
