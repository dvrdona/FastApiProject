from fastapi import APIRouter
from database.productservice import *

category_router = APIRouter(prefix="/category", tags=["Category"])


@category_router.post("/add_category")
async def add_category_api(name: str, description: str = None, image_url: str = None):
    result = add_category_db(name, description, image_url)
    return result


@category_router.get("/get_all_categories")
async def get_all_categories_api():
    return get_all_categories_db()


@category_router.get("/get_category")
async def get_category_api(category_id: str):
    result = get_category_db(category_id)
    return result


@category_router.put("/update_category")
async def update_category_api(category_id: int, name: str = None, description: str = None, image_url: str = None):
    result = update_category_db(category_id, name, description, image_url)
    return result


@category_router.delete('/delete_category')
async def delete_category_api(category_id: int):
    result = delete_category_db(category_id)
    return result