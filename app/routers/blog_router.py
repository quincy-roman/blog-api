from typing import Optional

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from models import Blog, Comment, UpdateBlog
from services import (convert_to_encodable, delete, find_all, find_one, insert,
                      update)

router = APIRouter(prefix='/blogs')
collection = 'blogs'


@router.get('/', response_description='List all blogs', response_model=Blog)
async def get_all_blogs(limit: int = 1000, published: bool = True, author: Optional[str] = None):
    search_query = {'published': published}
    if author:
        search_query['author'] = author

    blogs = await find_all(collection, search_query, limit)

    return JSONResponse(status_code=status.HTTP_200_OK, content=blogs)


@router.post('/', response_description='Post a blog', response_model=Blog)
async def post_blog(blog: Blog = Body(...)):
    created_blog = await insert(collection, blog)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_blog)


@router.post('/{id}/comments', response_description="Add a comment to a blog post", response_model=Blog)
async def add_comment(id: str, comment: Comment = Body(...)):
    comment = convert_to_encodable(comment)

    query_params = {'id': id, 'query': {'$push': {'comments': comment}}}
    result = await update(collection, comment, **query_params)

    if result:
        return result

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@router.get('/{id}', response_description='Get a single blog', response_model=Blog)
async def get_blog(id: str):
    blog = await find_one(collection, {'_id': id})

    if blog:
        return blog

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@router.put('/{id}', response_description='Update a blog', response_model=Blog)
async def update_blog(id: str, blog: UpdateBlog = Body(...)):
    blog = convert_to_encodable(blog)

    query_params = {'id': id, 'query': {'$set': blog}}
    result = await update(collection, blog, **query_params)

    if result:
        return result

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@router.delete('/{id}', response_description='Delete a blog')
async def delete_blog(id: str):
    if (await delete(collection, {'_id': id})):
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


# Following needs to be a PUT instead of DELETE for MongoDB, need full Comment object
@router.put('/{id}/comments', response_description="Delete a comment from a blog post", response_model=Blog)
async def delete_comment(id: str, comment: Comment = Body(...)):
    comment = convert_to_encodable(comment)

    query_params = {'id': id, 'query': {'$pull': {'comments': comment}}}
    result = await update(collection, comment, **query_params)

    if result:
        return result

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')
