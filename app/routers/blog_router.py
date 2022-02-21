from typing import List, Optional

from dependencies import get_current_active_user
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from models import Blog, Comment, UpdateBlog, User

router = APIRouter(
    prefix='/blogs',
    dependencies=[Depends(get_current_active_user)],
    tags=['blogs'])

collection = 'blogs'


@router.get('', response_description='List all blogs', response_model=List[UpdateBlog])
async def get_all_blogs(limit: int = 1000, published: bool = True, author: Optional[str] = None):
    search_query = {'published': published}
    if author:
        search_query['author'] = author

    blogs = await Blog.find(search_query, limit=limit).to_list()

    return blogs


@router.post('', response_description='Post a blog', response_model=UpdateBlog, status_code=201)
async def post_blog(blog: Blog = Body(...), current_user: User = Depends(get_current_active_user)):
    blog.author = current_user.username
    created_blog = await blog.insert()
    return created_blog


@router.post('/{id}/comments', response_description="Add a comment to a blog post", response_model=UpdateBlog, status_code=201)
async def add_comment(id: str, comment: Comment = Body(...), current_user: User = Depends(get_current_active_user)):
    blog = await Blog.get(id)
    if not blog:
        raise HTTPException(status_code=404, detail=f'Blog {id} not found')

    comment.author = current_user.username
    blog.comments.append(comment)
    await blog.replace()

    return blog


@router.get('/{id}', response_description='Get a single blog', response_model=UpdateBlog)
async def get_blog(id: str):
    blog = await Blog.get(id)

    if blog:
        return blog

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@router.put('/{id}', response_description='Update a blog', response_model=UpdateBlog)
async def update_blog(id: str, updated_blog: UpdateBlog = Body(...)):
    blog = await Blog.get(id)
    if not blog:
        raise HTTPException(status_code=404, detail=f'Blog {id} not found')

# TODO This need to be blog, not updated_blog
    blog = blog.copy(update=updated_blog.dict(exclude_unset=True))
    await blog.save()

    return blog


@router.delete('/{id}', response_description='Delete a blog')
async def delete_blog(id: str):
    blog = await Blog.get(id)
    if not blog:
        raise HTTPException(status_code=404, detail=f'Blog {id} not found')

    await blog.delete()
    return JSONResponse(status_code=204)


# Following needs to be a PUT instead of DELETE for MongoDB, need full Comment object
@router.put('/{id}/comments', response_description="Delete a comment from a blog post", response_model=UpdateBlog)
async def delete_comment(id: str, comment: Comment = Body(...)):
    blog = await Blog.get(id)

    if not blog:
        raise HTTPException(status_code=404, detail=f'Blog {id} not found')

    blog.comments.remove(comment)
    await blog.replace()

    return blog
