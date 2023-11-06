from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User
from src.schemas import ResponseHuman, HumanModel
from src.repository import humans as repository_humans
from src.services.auth import auth_service


router = APIRouter(prefix='/humans', tags=['Humans'])


@router.get("/", response_model=List[ResponseHuman], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_humans(limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_humans function returns a list of humans.

    :param limit: int: Limit the number of results returned
    :param le: Limit the number of humans returned
    :param offset: int: Specify the number of humans to skip
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A list of humans
    """
    humans = await repository_humans.get_humans(limit, offset, current_user, db)
    return humans


@router.get("/{human_id}", response_model=ResponseHuman)
async def get_human(human_id: int = Path(ge=1), db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_human function returns a human object with the given id.
    If the user is not logged in, they will be redirected to login page.
    If no human exists with that id, an HTTP 404 error is returned.

    :param human_id: int: Specify the human id to be passed in as a path parameter
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A human object
    """
    human = await repository_humans.get_human(human_id, current_user, db)
    if human is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.get("/search_name/", response_model=List[ResponseHuman])
async def get_human_name(human_name: str = Query(title="Name"), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_human_name function is used to get a human by name.
        The function takes in the human's name as an argument and returns the corresponding human object.

    :param human_name: str: Get the human_name from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A human object with the name that is passed in
    """
    human = await repository_humans.get_human_name(human_name, current_user, db)
    if not human:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.get("/search_surname/", response_model=List[ResponseHuman])
async def get_human_surname(human_surname: str = Query(title="Surname"), db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_human_surname function is used to get a human by surname.
        The function takes in the surname of the human as an argument and returns a list of humans with that surname.

    :param human_surname: str: Get the surname of a human from the database
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A list of all humans with a specified surname
    """
    human = await repository_humans.get_human_surname(human_surname, current_user, db)
    if not human:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.get("/search_email/", response_model=List[ResponseHuman])
async def get_human_email(human_email: str = Query(title="Email"), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_human_email function is used to get a human by email.
        The function takes in an email as a parameter and returns the human with that email.

    :param human_email: str: Get the human's email from the request
    :param db: Session: Connect to the database
    :param current_user: User: Get the current user from the database
    :return: A human object
    """
    human = await repository_humans.get_human_email(human_email, current_user, db)
    if not human:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.get("/list_birthday/", response_model=List[ResponseHuman])
async def get_list_birthdays(db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_list_birthdays function returns a list of humans with birthdays in the current month.

    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user from the database
    :return: A list of humans with their birthdays
    """
    humans = await repository_humans.get_list_birthdays(current_user, db)
    if not humans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return humans


@router.post("/", response_model=ResponseHuman, status_code=status.HTTP_201_CREATED)
async def create_human(body: HumanModel, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_human function creates a new human in the database.
        The function takes a HumanModel object as input, which is validated by pydantic.
        The function also takes an optional db Session object and current_user User object as inputs,
            both of which are provided by dependency injection via FastAPI's Depends() decorator.

    :param body: HumanModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A human object
    """
    human = await repository_humans.create_human(body, current_user, db)
    return human


@router.put("/{human_id}", response_model=ResponseHuman)
async def update_human(body: HumanModel, human_id: int = Path(ge=1), db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_human function updates a human in the database.
        The function takes an id and a body as input, which is then used to update the human in the database.
        If no human with that id exists, it returns 404 Not Found.

    :param body: HumanModel: Get the data from the request body
    :param human_id: int: Get the id of the human to be deleted
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: The updated human
    """
    human = await repository_humans.update_human(body, human_id, current_user, db)
    if human is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.delete("/{human_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_human(human_id: int = Path(ge=1), db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_human function removes a human from the database.
        The function takes in an integer representing the id of the human to be removed,
        and returns a dictionary containing information about that human.

    :param human_id: int: Specify the human id to be deleted
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: The removed human
    """
    human = await repository_humans.remove_human(human_id, current_user, db)
    if human is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human
