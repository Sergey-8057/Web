from datetime import date, datetime

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


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
