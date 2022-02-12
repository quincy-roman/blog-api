from fastapi import Body, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from db import db
from models import Blog, UpdateBlog

app = FastAPI()


@app.get('/blogs', response_description='List all blogs', response_model=Blog)
async def get_all_blogs():
    blogs = await db['blogs'].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=blogs)


@app.post('/blogs', response_description='Post a blog', response_model=Blog)
async def post_blog(blog: Blog = Body(...)):
    blog = jsonable_encoder(blog)
    new_blog = await db['blogs'].insert_one(blog)
    created_blog = await db['blogs'].find_one({"_id": new_blog.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_blog)


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
async def delete_student(id: str):
    delete_result = await db['blogs'].delete_one({'_id': id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'Blog {id} not found')
