from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from .pyObjectId import PyObjectId


class Comment(BaseModel):
    author: str = Field(...)
    body: str = Field(...)


class Blog(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    author: str = Field(...)
    title: str = Field(...)
    body: str = Field(...)
    published: bool = Field(...)
    comments: Optional[List[Comment]] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True
        schema_extra = {
            "example": {
                "author": "Username",
                "title": "Blog Title",
                "body": "Content of the blog post",
                "published": True,
                "comments": [
                    {
                        "author": "other.Username",
                        "body": "This is the comment body."
                    },
                    {
                        "author": "another.Username",
                        "body": "This is another comment body."
                    }
                ]
            }
        }


class UpdateBlog(BaseModel):
    author: Optional[str]
    title: Optional[str]
    body: Optional[str]
    published: Optional[bool]
    comments: Optional[List[Comment]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "author": "Username",
                "title": "Blog Title",
                "body": "Content of the blog post",
                "published": True,
                "comments": [
                    {
                        "author": "Other Username",
                        "body": "This is the comment body."
                    },
                    {
                        "author": "anothaUser",
                        "body": "This is another comment body."
                    }
                ]
            }
        }
