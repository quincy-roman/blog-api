from typing import Any

# from db import db
from fastapi.encoders import jsonable_encoder

# async def find_all(collection: str, search_query: str, limit: int):
#     return await db[collection].find(search_query).to_list(limit)


# async def find_one(collection: str, search_query: dict):
#     if(doc := await db[collection].find_one(search_query)) is not None:
#         return doc


# async def insert(collection: str, to_save: Any):
#     to_save = jsonable_encoder(to_save)
#     new_doc = await db[collection].insert_one(to_save)
#     return await db[collection].find_one({'_id': new_doc.inserted_id})


# async def update(collection: str, to_update: Any, **params):
#     id, query = params['id'], params['query']
#     id_query = {'_id': id}

#     if len(to_update) >= 1:
#         update_result = await db[collection].update_one(id_query, query)

#         if update_result.modified_count == 1:
#             if(updated_doc := await db[collection].find_one(id_query)) is not None:
#                 return updated_doc

#     if (existing_doc := await db[collection].find_one(id_query)) is not None:
#         return existing_doc

#     return None


# async def delete(collection: str, delete_query: dict):
#     delete_result = await db[collection].delete_one(delete_query)

#     return delete_result.deleted_count == 1


def convert_to_encodable(obj: Any):
    return {k: v for k, v in obj.dict().items() if v is not None}
