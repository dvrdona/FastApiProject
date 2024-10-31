from fastapi import APIRouter, HTTPException
from database.productservice import *
from typing import Optional

payment_router = APIRouter(prefix="/payment", tags=["Payment"])


@payment_router.post("/create")
async def create_payment_api(
    order_id: int,
    amount: float,
    payment_method: str,
    transaction_id: Optional[str] = None
):
    result = create_payment_db(
        order_id=order_id,
        amount=(str(amount)),  # Convert float to Decimal for precision
        payment_method=payment_method,
        transaction_id=transaction_id
    )
    if result:
        return {"status": "success", "payment_id": result}
    raise HTTPException(status_code=400, detail="Failed to create payment")


@payment_router.get("/get/{payment_id}")
async def get_payment_api(payment_id: int):
    result = get_payment_db(payment_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Payment not found")


@payment_router.get("/get_order_payment/{order_id}")
async def get_order_payment_api(order_id: int):
    result = get_order_payment_db(order_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Payment not found for this order")


@payment_router.put("/update_status/{payment_id}")
async def update_payment_status_api(
    payment_id: int,
    transaction_id: str
):
    result = update_payment_status_db(payment_id, transaction_id)
    if result:
        return {"status": "success", "message": "Payment status updated successfully"}
    raise HTTPException(status_code=404, detail="Payment not found")


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
            raise HTTPException(status_code=404, detail="Cart not found")

        cart_items = db.query(CartItem).filter_by(cart_id=cart.id).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

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
        raise HTTPException(status_code=404, detail="Order not found")
    return result