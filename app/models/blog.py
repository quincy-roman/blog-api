from typing import List, Optional

from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, Field


class Comment(BaseModel):
    author: Optional[str] = None
    body: str = Field(...)


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


class Blog(Document, UpdateBlog):

    @classmethod
    async def by_id(cls, id: str) -> "Blog":
        """Query by _id"""
        return await cls.find_one(Blog.id == id)

    class Collection:
        name = 'blogs'

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        orm_mode = True
        schema_extra = {
            "example": {
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
