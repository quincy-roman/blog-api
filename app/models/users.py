from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from .pyObjectId import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    first_name: str
    last_name: str
    email: EmailStr

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


class UserInDB(User):
    hashed_pass: str


class UpdateUser(BaseModel):
    username: Optional[str]
    pass_hash: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Username",
                "pass_hash": "$2b$12$Pk/Pg2ZLFMZGkmRCbkLWVeH6fvbCjHhr3cAHdyDHiNEz./PgBanwO",
                "first_name": "Jason",
                "last_name": "Jackson",
                "email": "jason.jackson@gmail.com"
            }
        }
