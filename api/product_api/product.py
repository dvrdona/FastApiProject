from fastapi import APIRouter
from database.productservice import *
from typing import Optional


product_router = APIRouter(prefix="/product", tags=["Product"])


@product_router.post("/add_product")
async def add_product_api(
        category_id:int,
        name: str,
        price: float,
        description: Optional[str] = None,
        stock_quantity: int = 0,
        image_url: Optional[str] = None,
        is_available: bool = True
):
    result = add_product_db(
        category_id=category_id,
        name=name,
        price=price,
        description=description,
        stock_quantity=stock_quantity,
        image_url=image_url,
        is_available=is_available
    )
    return result


@product_router.get("/get_all_products")
async def get_all_products_api():
    return get_all_products_db()


@product_router.get("/get_product")
async def get_product_api(product_id: int):
    result = get_product_db(product_id)
    return result


@product_router.get("/get_products_by_category")
async def get_products_by_category_api(category_id: int):
    result = get_products_by_category_db(category_id)
    return result


@product_router.put("/update_product")
async def update_product_api( product_id: int, category_id: Optional[int] = None,
        name: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
        stock_quantity: Optional[int] = None,
        image_url: Optional[str] = None,
        is_available: Optional[bool] = None
):
    update_data = {
        key: value
        for key, value in {
            'category_id': category_id,
            'name': name,
            'price': price,
            'description': description,
            'stock_quantity': stock_quantity,
            'image_url': image_url,
            'is_available': is_available
        }.items()
        if value is not None
    }

    result = update_product_db(product_id, **update_data)
    return result


@product_router.delete('/delete_product')
async def delete_product_api(product_id: int):
    result = delete_product_db(product_id)
    return result