from sqlalchemy import (Column, String, Integer, BigInteger, DateTime, ForeignKey, Numeric, Boolean)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
   __tablename__ = "users"

   id = Column(BigInteger, autoincrement=True, primary_key=True)
   username = Column(String, nullable=False)
   email = Column(String, nullable=False, unique=True)
   password = Column(String, nullable=False)
   phone = Column(String, nullable=True)
   address = Column(String, nullable=True)
   city = Column(String, nullable=True)
   reg_date = Column(DateTime, default=datetime.now())
   is_active = Column(Boolean, default=True)

   orders = relationship("Order", back_populates="user")
   cart = relationship("Cart", back_populates="user", uselist=False)

class Category(Base):
   __tablename__ = "categories"

   id = Column(Integer, autoincrement=True, primary_key=True)
   name = Column(String, nullable=False)
   description = Column(String, nullable=True)
   image_url = Column(String, nullable=True)

   products = relationship("Product", back_populates="category")

class Product(Base):
   __tablename__ = "products"

   id = Column(Integer, autoincrement=True, primary_key=True)
   category_id = Column(Integer, ForeignKey("categories.id"))
   name = Column(String, nullable=False)
   description = Column(String, nullable=True)
   price = Column(Numeric(10, 2), nullable=False)
   stock_quantity = Column(Integer, nullable=False, default=0)
   image_url = Column(String, nullable=True)
   is_available = Column(Boolean, default=True)
   created_at = Column(DateTime, default=datetime.now())
   updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

   category = relationship("Category", back_populates="products")
   cart_items = relationship("CartItem", back_populates="product")
   order_items = relationship("OrderItem", back_populates="product")

class Cart(Base):
   __tablename__ = "carts"

   id = Column(Integer, autoincrement=True, primary_key=True)
   user_id = Column(BigInteger, ForeignKey("users.id"))
   created_at = Column(DateTime, default=datetime.now())
   updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

   user = relationship("User", back_populates="cart")
   items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
   __tablename__ = "cart_items"

   id = Column(Integer, autoincrement=True, primary_key=True)
   cart_id = Column(Integer, ForeignKey("carts.id"))
   product_id = Column(Integer, ForeignKey("products.id"))
   quantity = Column(Integer, nullable=False, default=1)
   added_at = Column(DateTime, default=datetime.now())

   cart = relationship("Cart", back_populates="items")
   product = relationship("Product", back_populates="cart_items")

class Order(Base):
   __tablename__ = "orders"

   id = Column(Integer, autoincrement=True, primary_key=True)
   user_id = Column(BigInteger, ForeignKey("users.id"))
   total_amount = Column(Numeric(10, 2), nullable=False)
   #status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
   shipping_address = Column(String, nullable=False)
   shipping_city = Column(String, nullable=False)
   shipping_postal_code = Column(String, nullable=False)
   created_at = Column(DateTime, default=datetime.now())
   updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

   user = relationship("User", back_populates="orders")
   items = relationship("OrderItem", back_populates="order")
   payment = relationship("Payment", back_populates="order", uselist=False)

class OrderItem(Base):
   __tablename__ = "order_items"

   id = Column(Integer, autoincrement=True, primary_key=True)
   order_id = Column(Integer, ForeignKey("orders.id"))
   product_id = Column(Integer, ForeignKey("products.id"))
   quantity = Column(Integer, nullable=False)
   price = Column(Numeric(10, 2), nullable=False)  # Цена на момент заказа

   order = relationship("Order", back_populates="items")
   product = relationship("Product", back_populates="order_items")

class Payment(Base):
   __tablename__ = "payments"

   id = Column(Integer, autoincrement=True, primary_key=True)
   order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
   amount = Column(Numeric(10, 2), nullable=False)
   #status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
   payment_method = Column(String, nullable=False)  # "card", "paypal" и т.д.
   transaction_id = Column(String, nullable=True)  # ID транзакции от платежной системы
   created_at = Column(DateTime, default=datetime.now())
   updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

   order = relationship("Order", back_populates="payment")