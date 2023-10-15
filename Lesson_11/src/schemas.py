from datetime import date

from pydantic import BaseModel, EmailStr, Field


class HumanModel(BaseModel):
	name: str = Field("Tom", min_length=1, max_length=20)
	surname: str = Field("Cruise", min_length=1, max_length=20)
	email: EmailStr
	phone: str = Field(min_length=10, max_length=13)
	birthday: date
	description: str


class ResponseHuman(BaseModel):
	id: int
	name: str
	surname: str
	email: EmailStr
	phone: str
	birthday: date
	description: str


	class Config:
		from_attributes = True
