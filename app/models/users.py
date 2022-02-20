from typing import Optional

from beanie import Document
from bson import ObjectId
from pydantic import EmailStr, Field


class User(Document):
    username: str = Field(...)
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    disabled: Optional[bool]

    class Collection:
        name = 'users'

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Username",
                "hashed_pass": "plaintext pass, this will be hashed",
                "first_name": "Jason",
                "last_name": "Jackson",
                "email": "jason.jackson@gmail.com",
                "disabled": True
            }
        }


class UserInDB(User):
    hashed_pass: str
