from typing import Optional

from fastapi import Body, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from db import db
from models import Blog, Comment, UpdateBlog

app = FastAPI()


@app.get('/blogs', response_description='List all blogs', response_model=Blog)
async def get_all_blogs(limit: int = 1000, published: bool = True, author: Optional[str] = None):
    search_query = {'published': published}
    if author:
        search_query['author'] = author

    blogs = await db['blogs'].find(search_query).to_list(limit)

    return JSONResponse(status_code=status.HTTP_200_OK, content=blogs)


@app.post('/blogs', response_description='Post a blog', response_model=Blog)
async def post_blog(blog: Blog = Body(...)):
    blog = jsonable_encoder(blog)
    new_blog = await db['blogs'].insert_one(blog)
    created_blog = await db['blogs'].find_one({"_id": new_blog.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_blog)


@app.post('/blogs/{id}/comments', response_description="Add a comment to a blog post", response_model=Blog)
async def add_comment(id: str, comment: Comment = Body(...)):
    comment = {k: v for k, v in comment.dict().items() if v is not None}

    if len(comment) >= 1:
        update_result = await db['blogs'].update_one({'_id': id}, {'$push': {'comments': comment}})

        if update_result.modified_count == 1:
            if (updated_blog := await db['blogs'].find_one({'_id': id})) is not None:
                return updated_blog

    if (existing_blog := await db['blogs'].find_one({'_id': id})) is not None:
        return existing_blog

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@app.get('/blogs/{id}', response_description='Get a single blog', response_model=Blog)
async def get_blog(id: str):
    if(blog := await db['blogs'].find_one({'_id': id})) is not None:
        return blog

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@app.put('/blogs/{id}', response_description='Update a blog', response_model=Blog)
async def update_blog(id: str, blog: UpdateBlog = Body(...)):
    blog = {k: v for k, v in blog.dict().items() if v is not None}

    if len(blog) >= 1:
        update_result = await db['blogs'].update_one({'_id': id}, {'$set': blog})

        if update_result.modified_count == 1:
            if (updated_blog := await db['blogs'].find_one({'_id': id})) is not None:
                return updated_blog

    if (existing_blog := await db['blogs'].find_one({'_id': id})) is not None:
        return existing_blog

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


@app.delete('/blogs/{id}', response_description='Delete a blog')
async def delete_blog(id: str):
    delete_result = await db['blogs'].delete_one({'_id': id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')


# Following needs to be a PUT instead of DELETE for MongoDB, need full Comment object
@app.put('/blogs/{id}/comments', response_description="Delete a comment from a blog post", response_model=Blog)
async def delete_comment(id: str, comment: Comment = Body(...)):
    comment = {k: v for k, v in comment.dict().items() if v is not None}

    update_result = await db['blogs'].update_one({'_id': id}, {'$pull': {'comments': comment}})

    if update_result.modified_count == 1:
        if (updated_blog := await db['blogs'].find_one({'_id': id})) is not None:
            return updated_blog

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')
