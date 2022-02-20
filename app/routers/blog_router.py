from typing import Optional

from dependencies import get_current_active_user
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import Blog, Comment, UpdateBlog, User
from services import convert_to_encodable

router = APIRouter(
    prefix='/blogs',
    dependencies=[Depends(get_current_active_user)],
    tags=['blogs'])

collection = 'blogs'


@router.get('', response_description='List all blogs', response_model=Blog)
async def get_all_blogs(limit: int = 1000, published: bool = True, author: Optional[str] = None):
    search_query = {'published': published}
    if author:
        search_query['author'] = author

    # blogs = await find_all(collection, search_query, limit)
    blogs = await Blog.find(search_query, limit=limit).to_list()

    return JSONResponse(status_code=status.HTTP_200_OK, content=blogs)


@router.post('', response_description='Post a blog', response_model=Blog)
async def post_blog(blog: Blog = Body(...), current_user: User = Depends(get_current_active_user)):
    blog.author = current_user.username
    # created_blog = await insert(collection, blog)
    created_blog = await blog.insert()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_blog)


@router.post('/{id}/comments', response_description="Add a comment to a blog post", response_model=Blog)
async def add_comment(id: str, comment: Comment = Body(...)):
    comment = convert_to_encodable(comment)

    # query_params = {'id': id, 'query': {'$push': {'comments': comment}}}
    # result = await update(collection, comment, **query_params)
    blog = await Blog.find_one(Blog.id == id)
    blog.comments.append(comment)
    result = await blog.replace()

    if result:
        return result

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@router.get('/{id}', response_description='Get a single blog', response_model=Blog)
async def get_blog(id: str):
    # blog = await find_one(collection, {'_id': id})
    blog = await Blog.find_one(Blog.id == id)

    if blog:
        return blog

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@router.put('/{id}', response_description='Update a blog', response_model=Blog)
async def update_blog(id: str, blog: UpdateBlog = Body(...)):
    # blog = convert_to_encodable(blog)

    # query_params = {'id': id, 'query': {'$set': blog}}
    # result = await update(collection, blog, **query_params)
    blog.id = id
    result = await blog.replace()

    if result:
        return result

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@router.delete('/{id}', response_description='Delete a blog')
async def delete_blog(id: str):
    # if (await delete(collection, {'_id': id})):
    if await Blog.find_one(Blog.id == id).delete():
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


# Following needs to be a PUT instead of DELETE for MongoDB, need full Comment object
@router.put('/{id}/comments', response_description="Delete a comment from a blog post", response_model=Blog)
async def delete_comment(id: str, comment: Comment = Body(...)):
    # comment = convert_to_encodable(comment)

    # query_params = {'id': id, 'query': {'$pull': {'comments': comment}}}
    # result = await update(collection, comment, **query_params)
    blog = await Blog.find_one(Blog.id == id)
    blog.comments.remove(comment)
    result = await blog.replace()

    if result:
        return result

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')
