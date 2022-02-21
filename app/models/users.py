from typing import Optional

from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


# Didn't try, but this should help. Make sure to update to use UserInDB for db calls.
class User(BaseModel):
    username: str = Field(...)
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    disabled: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Username",
                "first_name": "Jason",
                "last_name": "Jackson",
                "email": "jason.jackson@gmail.com"
            }
        }


class UserInDB(Document, User):
    hashed_pass: str

    @classmethod
    async def by_username(cls, username: str) -> "UserInDB":
        """Query by username helper method

        Args:
            username (str): username to query by

        Returns:
            UserInDB: User matching the query
        """
        return await cls.find_one(cls.username == username)

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
                "email": "jason.jackson@gmail.com"
            }
        }
