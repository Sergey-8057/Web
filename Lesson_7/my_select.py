from pprint import pprint
from sqlalchemy import func, desc, and_, distinct, select

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_1():
    """
    Найти 5 студентов с наибольшим средним баллом по всем предметам.
    """
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()
    return result


def select_2(num_disc):
    """
    Найти студента с наивысшим средним баллом по определенному предмету. 
    """
    result = session.query(Student.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .where(Discipline.id == num_disc) \
        .group_by(Student.id) \
        .group_by(Discipline.id) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return result


def select_3(num_disc):
    """
    Найти средний балл в группах по определенному предмету.
    """
    result = session.query(Discipline.name, Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Student) \
        .join(Group) \
        .where(Discipline.id == num_disc) \
        .group_by(Group.id) \
        .group_by(Discipline.id) \
        .order_by(desc('avg_grade')) \
        .all()
    return result


def select_4():
    """
    Найти средний балл на потоке (по всей таблице оценок).
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .all()
    return result


def select_5(num_teach):
    """
    Найти какие курсы читает определенный преподаватель.
    """
    result = session.query(Teacher.fullname, Discipline.name) \
        .select_from(Teacher) \
        .join(Discipline) \
        .where(Teacher.id == num_teach) \
        .order_by(Discipline.name) \
        .all()
    return result


def select_6(num_group):
    """
    Найти список студентов в определенной группе.
    """
    result = session.query(Group.name, Student.fullname) \
        .select_from(Group) \
        .join(Student) \
        .where(Group.id == num_group) \
        .order_by(Student.fullname) \
        .all()
    return result


def select_7(num_group, num_disc):
    """
    Найти оценки студентов в отдельной группе по определенному предмету.
    """
    result = session.query(Group.name, Discipline.name, Student.fullname, Grade.grade) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Student) \
        .join(Group) \
        .where(and_(Group.id == num_group, Discipline.id == num_disc)) \
        .order_by(Student.fullname) \
        .all()
    return result


def select_8(num_teach):
    """
    Найти средний балл, который ставит определенный преподаватель по своим предметам.
    """
    result = session.query(distinct(Teacher.fullname), func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .where(Teacher.id == num_teach) \
        .group_by(Teacher.fullname) \
        .order_by(desc('avg_grade')) \
        .all()
    return result


def select_9(num_stud):
    """
    Найти список курсов, которые посещает определенный студент.
    """
    result = session.query(distinct(Student.fullname), Discipline.name) \
        .select_from(Student) \
        .join(Grade) \
        .join(Discipline) \
        .where(Student.id == num_stud) \
        .order_by(Discipline.name) \
        .all()
    return result


def select_10(num_stud, num_teach):
    """
    Список курсов, которые определенному студенту читает определенный преподаватель.
    """
    result = session.query(distinct(Teacher.fullname), Discipline.name, Student.fullname) \
        .select_from(Teacher) \
        .join(Discipline) \
        .join(Grade) \
        .join(Student) \
        .where(and_(Student.id == num_stud, Teacher.id == num_teach)) \
        .order_by(Discipline.name) \
        .all()
    return result


def select_11(num_teach, num_stud):
    """
    Средний балл, который определенный преподаватель ставит определенному студенту.
    """
    result = session.query(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .join(Student) \
        .where(and_(Teacher.id == num_teach, Student.id == num_stud)) \
        .group_by(Student.id) \
        .group_by(Teacher.id) \
        .all()
    return result


def select_12():
    """
    Оценки студентов в определенной группе по определенному предмету на последнем занятии.
    """
    group_id = 2
    dis_id = 2
    # Знаходимо останнє заняття
    subq = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == dis_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1)).scalar_subquery()

    result = session.query(Student.fullname, Discipline.name, Group.name, Grade.grade, Grade.date_of) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(and_(Grade.discipline_id == dis_id, Group.id == group_id, Grade.date_of == subq)) \
        .order_by(desc(Grade.date_of)).all()
    return result


if __name__ == '__main__':
    pprint(select_1())
    pprint(select_2(num_disc=5))
    pprint(select_3(num_disc=2))
    pprint(select_4())
    pprint(select_5(num_teach=5))
    pprint(select_6(num_group=1))
    pprint(select_7(num_group=2, num_disc=3))
    pprint(select_8(num_teach=4))
    pprint(select_9(num_stud=7))
    pprint(select_10(num_stud=18, num_teach=2))
    pprint(select_11(num_teach=2, num_stud=11))
    pprint(select_12())
