from datetime import date, datetime, timedelta
from typing import List

from sqlalchemy import and_, extract
from sqlalchemy.orm import Session

from src.database.models import Human, User
from src.schemas import HumanModel


async def get_humans(limit: int, offset: int, user: User, db: Session) -> List[Human]:
    """
    The get_humans function returns a list of humans from the database.

    :param limit: int: Limit the number of results returned
    :param offset: int: Specify the number of records to skip
    :param user: User: Get the user_id from the database
    :param db: Session: Create a database session
    :return: A list of humans
    """
    return db.query(Human).filter(Human.user_id == user.id).limit(limit).offset(offset).all()


async def get_human(human_id: int, user: User, db: Session) -> Human:
    """
    The get_human function returns a human object from the database.

    :param human_id: int: Get the human from the database
    :param user: User: Get the user that is making the request
    :param db: Session: Access the database
    :return: A single human object
    """
    return db.query(Human).filter(and_(Human.id == human_id, Human.user_id == user.id)).first()


async def get_human_name(human_name: str, user: User, db: Session) -> List[Human]:
    """
    The get_human_name function takes in a human name and returns all humans with that name.

    :param human_name: str: Filter the database by name
    :param user: User: Get the user_id from the user object
    :param db: Session: Create a database session
    :return: A list of humans
    """
    return db.query(Human).filter(and_(Human.name == human_name, Human.user_id == user.id)).all()


async def get_human_surname(human_surname: str, user: User, db: Session) -> List[Human]:
    """
    The get_human_surname function returns a list of humans with the given surname.
        Args:
            human_surname (str): The surname of the human to be returned.
            user (User): The user who is making this request. This is used for authorization purposes, as only users can access their own data in this application.
            db (Session): A database session object that allows us to query and manipulate our database objects without having to create new sessions each time we want to do so.

    :param human_surname: str: Filter the results by surname
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A list of all humans with the given surname
    """
    return db.query(Human).filter(and_(Human.surname == human_surname, Human.user_id == user.id)).all()


async def get_human_email(human_email: str, user: User, db: Session) -> List[Human]:
    """
    The get_human_email function takes in a human_email and user, and returns all humans with that email.

    :param human_email: str: Filter the query by email
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of humans
    """
    return db.query(Human).filter(and_(Human.email == human_email, Human.user_id == user.id)).all()


async def get_list_birthdays(user: User, db: Session) -> List[Human]:
    """
    The get_list_birthdays function returns a list of humans whose birthday is in the next 7 days.

    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A list of humans whose birthday is in the next 7 days
    """
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
    """
    The create_human function creates a new human in the database.

    :param body: HumanModel: Create a new human object
    :param user: User: Get the user who is making the request
    :param db: Session: Access the database
    :return: A human object
    """
    human = Human(**body.dict(), user=user)
    db.add(human)
    db.commit()
    db.refresh(human)
    return human


async def update_human(body: HumanModel, human_id: int, user: User, db: Session) -> Human | None:
    """
    The update_human function updates a human in the database.
        Args:
            body (HumanModel): The HumanModel object to be updated.
            human_id (int): The id of the Human to be updated.
            user (User): The User who is updating this Human, used for authorization purposes.

    :param body: HumanModel: Get the data from the request body
    :param human_id: int: Find the human in the database
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: A human object
    """
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
    """
    The remove_human function removes a human from the database.
        Args:
            human_id (int): The id of the human to remove.
            user (User): The user who is removing this human.

    :param human_id: int: Specify the id of the human to be removed
    :param user: User: Identify the user who is making the request
    :param db: Session: Connect to the database
    :return: The human object that was deleted
    """
    human = db.query(Human).filter(and_(Human.id == human_id, Human.user_id == user.id)).first()
    if human:
        db.delete(human)
        db.commit()
    return human
