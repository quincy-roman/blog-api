from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from .pyObjectId import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    disabled: Optional[bool]

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
