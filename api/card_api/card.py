from fastapi import APIRouter
from database.productservice import *


cart_router = APIRouter(prefix="/cart", tags=["Cart"])


@cart_router.get("/get_cart")
async def get_or_create_cart_api(user_id: int):
    result = get_or_create_cart_db(user_id)
    return result


@cart_router.post("/add_item")
async def add_to_cart_api(
    user_id: int,
    product_id: int,
    quantity: int = 1
):
    result = add_to_cart_db(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )
    return result


@cart_router.get("/get_items")
async def get_cart_items_api(user_id: int):
    result = get_cart_items_db(user_id)
    return result


@cart_router.put("/update_item")
async def update_cart_item_api(
    user_id: int,
    product_id: int,
    quantity: int
):
    result = update_cart_item_db(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )
    return result

@cart_router.delete("/remove_item")
async def remove_from_cart_api(
    user_id: int,
    product_id: int
):
    result = remove_from_cart_db(
        user_id=user_id,
        product_id=product_id
    )
    return result


order_router = APIRouter(prefix="/order", tags=["Order"])


@order_router.post("/create")
async def create_order_api(
        user_id: int,
        total_amount: float,
        shipping_address: str,
        shipping_city: str,
        shipping_postal_code: str
):
    with next(get_db()) as db:
        cart = db.query(Cart).filter_by(user_id=user_id).first()
        if not cart:
            return "Cart not found"

        cart_items = db.query(CartItem).filter_by(cart_id=cart.id).all()
        if not cart_items:
            return "Cart is empty"

    result = create_order_db(
        user_id=user_id,
        total_amount=int(str(total_amount)),
        shipping_address=shipping_address,
        shipping_city=shipping_city,
        shipping_postal_code=shipping_postal_code,
        cart_items=cart_items
    )
    return {"order_id": result}


@order_router.get("/user/{user_id}")
async def get_user_orders_api(user_id: int):
    return get_user_orders_db(user_id)


@order_router.get("/details/{order_id}")
async def get_order_details_api(order_id: int):
    result = get_order_details_db(order_id)
    if not result:
        return "Order not found"
    return result