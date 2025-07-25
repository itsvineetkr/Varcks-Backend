from pydantic import BaseModel
from src.database.mongo import db


users = db.users


class User(BaseModel):
    username: str
    email: str
    full_name: str
    hashed_password: str
    disabled: bool = False


class CreateUser(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    disabled: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(BaseModel):
    hashed_password: str
