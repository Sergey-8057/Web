from datetime import date, datetime, timedelta

from sqlalchemy import and_, extract
from sqlalchemy.orm import Session

from src.database.models import Human
from src.schemas import HumanModel


async def get_humans(limit: int, offset: int, db: Session):
    humans = db.query(Human)
    humans = humans.limit(limit).offset(offset).all()
    return humans


async def get_human(human_id: int, db: Session):
    human = db.query(Human).filter_by(id=human_id).first()
    return human


async def get_human_name(human_name: str, db: Session):
    human = db.query(Human).filter_by(name=human_name).all()
    return human


async def get_human_surname(human_surname: str, db: Session):
    human = db.query(Human).filter_by(surname=human_surname).all()
    return human


async def get_human_email(human_email: str, db: Session):
    human = db.query(Human).filter_by(email=human_email).all()
    return human


async def get_list_birthdays(db: Session):
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)
    if start_date.day <= end_date.day:
        humans = db.query(Human).filter(
            and_(
                extract('day', Human.birthday) >= start_date.day,
                extract('day', Human.birthday) <= end_date.day
                )
        ).all()
    else:
        # Если текущая дата ближе к концу месяца, выполняем два отдельных фильтра
        humans = db.query(Human).filter(
            and_(
                extract('month', Human.birthday) == start_date.month,
                extract('day', Human.birthday) >= start_date.day
            )
        ).union(
            db.query(Human).filter(
                and_(
                    extract('month', Human.birthday) == (start_date.month % 12) + 1,
                    extract('day', Human.birthday) <= end_date.day
                )
            )
        ).all()

    return humans


async def create_human(body: HumanModel, db: Session):
    human = Human(**body.dict())
    db.add(human)
    db.commit()
    db.refresh(human)
    return human


async def update_human(body: HumanModel, human_id: int, db: Session):
    human = db.query(Human).filter_by(id=human_id).first()
    if human:
        human.name = body.name
        human.surname = body.surname
        human.email = body.email
        human.phone = body.phone
        human.birthday = body.birthday
        human.description = body.description
        db.commit()
    return human


async def remove_human(human_id: int, db: Session):
    human = db.query(Human).filter_by(id=human_id).first()
    if human:
        db.delete(human)
        db.commit()
    return human
