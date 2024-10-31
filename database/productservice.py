from database.models import Category, Product, Cart, CartItem, Order, OrderItem, Payment
from database import get_db
from datetime import datetime

"""Category"""


def add_category_db(name, description=None, image_url=None):
    with next(get_db()) as db:
        new_category = Category(
            name=name,
            description=description,
            image_url=image_url
        )
        db.add(new_category)
        db.commit()
        return new_category.id


def get_all_categories_db():
    with next(get_db()) as db:
        return db.query(Category).all()


def get_category_db(category_id):
    with next(get_db()) as db:
        return db.query(Category).filter_by(id=category_id).first()


def update_category_db(category_id, name=None, description=None, image_url=None):
    with next(get_db()) as db:
        category = db.query(Category).filter_by(id=category_id).first()
        if category:
            if name:
                category.name = name
            if description is not None:
                category.description = description
            if image_url is not None:
                category.image_url = image_url
            db.commit()
            return True
        return False


def delete_category_db(category_id):
    with next(get_db()) as db:
        db.query(Category).filter_by(id=category_id).delete()
        db.commit()
        return True


"""Product"""


def add_product_db(category_id, name, price, description=None,
                   stock_quantity=0, image_url=None, is_available=True):
    with next(get_db()) as db:
        new_product = Product(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            image_url=image_url,
            is_available=is_available
        )
        db.add(new_product)
        db.commit()
        return new_product.id


def get_all_products_db():
    with next(get_db()) as db:
        return db.query(Product).all()


def get_product_db(product_id):
    with next(get_db()) as db:
        return db.query(Product).filter_by(id=product_id).first()


def get_products_by_category_db(category_id):
    with next(get_db()) as db:
        return db.query(Product).filter_by(category_id=category_id).all()


def update_product_db(product_id, **kwargs):
    with next(get_db()) as db:
        product = db.query(Product).filter_by(id=product_id).first()
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            product.updated_at = datetime.now()
            db.commit()
            return True
        return False


def delete_product_db(product_id):
    with next(get_db()) as db:
        db.query(Product).filter_by(id=product_id).delete()
        db.commit()
        return True


"""Cart"""


def get_or_create_cart_db(user_id):
    with next(get_db()) as db:
        cart = db.query(Cart).filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
        return cart


def add_to_cart_db(user_id, product_id, quantity=1):
    with next(get_db()) as db:
        cart = get_or_create_cart_db(user_id)
        cart_item = db.query(CartItem).filter_by(
            cart_id=cart.id,
            product_id=product_id
        ).first()

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)

        db.commit()
        return True


def get_cart_items_db(user_id):
    with next(get_db()) as db:
        cart = db.query(Cart).filter_by(user_id=user_id).first()
        if cart:
            return db.query(CartItem).filter_by(cart_id=cart.id).all()
        return []


def update_cart_item_db(user_id, product_id, quantity):
    with next(get_db()) as db:
        cart = db.query(Cart).filter_by(user_id=user_id).first()
        if cart:
            cart_item = db.query(CartItem).filter_by(
                cart_id=cart.id,
                product_id=product_id
            ).first()
            if cart_item:
                cart_item.quantity = quantity
                db.commit()
                return True
        return False


def remove_from_cart_db(user_id, product_id):
    with next(get_db()) as db:
        cart = db.query(Cart).filter_by(user_id=user_id).first()
        if cart:
            db.query(CartItem).filter_by(
                cart_id=cart.id,
                product_id=product_id
            ).delete()
            db.commit()
            return True
        return False


"""Order"""


def create_order_db(user_id, total_amount, shipping_address,
                    shipping_city, shipping_postal_code, cart_items):
    with next(get_db()) as db:
        # Создаем заказ
        new_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code
        )
        db.add(new_order)
        db.flush()  # Получаем id заказа

        # Добавляем товары из корзины в заказ
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.add(order_item)

        # Очищаем корзину
        cart = db.query(Cart).filter_by(user_id=user_id).first()
        if cart:
            db.query(CartItem).filter_by(cart_id=cart.id).delete()

        db.commit()
        return new_order.id


def get_user_orders_db(user_id):
    with next(get_db()) as db:
        return db.query(Order).filter_by(user_id=user_id).all()


def get_order_details_db(order_id):
    with next(get_db()) as db:
        return db.query(Order).filter_by(id=order_id).first()


"""Payment"""


def create_payment_db(order_id, amount, payment_method, transaction_id=None):
    with next(get_db()) as db:
        new_payment = Payment(
            order_id=order_id,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id
        )
        db.add(new_payment)
        db.commit()
        return new_payment.id


def get_payment_db(payment_id):
    with next(get_db()) as db:
        return db.query(Payment).filter_by(id=payment_id).first()


def get_order_payment_db(order_id):
    with next(get_db()) as db:
        return db.query(Payment).filter_by(order_id=order_id).first()


def update_payment_status_db(payment_id, transaction_id):
    with next(get_db()) as db:
        payment = db.query(Payment).filter_by(id=payment_id).first()
        if payment:
            payment.transaction_id = transaction_id
            payment.updated_at = datetime.now()
            db.commit()
            return True
        return False