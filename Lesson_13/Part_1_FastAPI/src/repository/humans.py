from datetime import date, datetime, timedelta
from typing import List

from sqlalchemy import and_, extract
from sqlalchemy.orm import Session

from src.database.models import Human, User
from src.schemas import HumanModel


async def get_humans(limit: int, offset: int, user: User, db: Session) -> List[Human]:
    return db.query(Human).filter(Human.user_id == user.id).limit(limit).offset(offset).all()


async def get_human(human_id: int, user: User, db: Session) -> Human:
    return db.query(Human).filter(and_(Human.id == human_id, Human.user_id == user.id)).first()


async def get_human_name(human_name: str, user: User, db: Session) -> List[Human]:
    return db.query(Human).filter(and_(Human.name == human_name, Human.user_id == user.id)).all()


async def get_human_surname(human_surname: str, user: User, db: Session) -> List[Human]:
    return db.query(Human).filter(and_(Human.surname == human_surname, Human.user_id == user.id)).all()


async def get_human_email(human_email: str, user: User, db: Session) -> List[Human]:
    return db.query(Human).filter(and_(Human.email == human_email, Human.user_id == user.id)).all()


async def get_list_birthdays(user: User, db: Session) -> List[Human]:
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)
    if start_date.day <= end_date.day:
        humans = db.query(Human).filter(
            and_(
                extract('day', Human.birthday) >= start_date.day,
                extract('day', Human.birthday) <= end_date.day,
                Human.user_id == user.id
                )
        ).all()
    else:
        # Если текущая дата ближе к концу месяца, выполняем два отдельных фильтра
        humans = db.query(Human).filter(
            and_(
                extract('month', Human.birthday) == start_date.month,
                extract('day', Human.birthday) >= start_date.day,
                Human.user_id == user.id
            )
        ).union(
            db.query(Human).filter(
                and_(
                    extract('month', Human.birthday) == (start_date.month % 12) + 1,
                    extract('day', Human.birthday) <= end_date.day,
                    Human.user_id == user.id
                )
            )
        ).all()
    return humans


async def create_human(body: HumanModel, user: User, db: Session) -> Human:
    human = Human(**body.dict(), user=user)
    db.add(human)
    db.commit()
    db.refresh(human)
    return human


async def update_human(body: HumanModel, human_id: int, user: User, db: Session) -> Human | None:
    human = db.query(Human).filter(and_(Human.id == human_id, Human.user_id == user.id)).first()
    if human:
        human.name = body.name
        human.surname = body.surname
        human.email = body.email
        human.phone = body.phone
        human.birthday = body.birthday
        human.description = body.description
        db.commit()
    return human


async def remove_human(human_id: int, user: User, db: Session) -> Human | None:
    human = db.query(Human).filter(and_(Human.id == human_id, Human.user_id == user.id)).first()
    if human:
        db.delete(human)
        db.commit()
    return human
