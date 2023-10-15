from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.schemas import ResponseHuman, HumanModel
from src.repository import humans as repository_humans


router = APIRouter(prefix='/humans', tags=['Humans'])


@router.get("/", response_model=List[ResponseHuman])
async def get_humans(limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db)):
    humans = await repository_humans.get_humans(limit, offset, db)
    return humans


@router.get("/{human_id}", response_model=ResponseHuman)
async def get_human(human_id: int = Path(ge=1), db: Session = Depends(get_db)):
    human = await repository_humans.get_human(human_id, db)
    if human is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.get("/search_name/", response_model=List[ResponseHuman])
async def get_human_name(human_name: str = Query(title="Name"), db: Session = Depends(get_db)):
    human = await repository_humans.get_human_name(human_name, db)
    if not human:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.get("/search_surname/", response_model=List[ResponseHuman])
async def get_human_surname(human_surname: str = Query(title="Surname"), db: Session = Depends(get_db)):
    human = await repository_humans.get_human_surname(human_surname, db)
    if not human:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.get("/search_email/", response_model=List[ResponseHuman])
async def get_human_email(human_email: str = Query(title="Email"), db: Session = Depends(get_db)):
    human = await repository_humans.get_human_email(human_email, db)
    if not human:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.get("/list_birthday/7days", response_model=List[ResponseHuman])
async def get_list_birthdays(db: Session = Depends(get_db)):
    humans = await repository_humans.get_list_birthdays(db)
    if not humans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return humans


@router.post("/", response_model=ResponseHuman, status_code=status.HTTP_201_CREATED)
async def create_human(body: HumanModel, db: Session = Depends(get_db)):
    human = await repository_humans.create_human(body, db)
    return human


@router.put("/{human_id}", response_model=ResponseHuman)
async def update_human(body: HumanModel, human_id: int = Path(ge=1), db: Session = Depends(get_db)):
    human = await repository_humans.update_human(body, human_id, db)
    if human is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human


@router.delete("/{human_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_human(human_id: int = Path(ge=1), db: Session = Depends(get_db)):
    human = await repository_humans.remove_human(human_id, db)
    if human is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return human
