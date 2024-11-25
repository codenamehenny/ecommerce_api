# This file establishes the table models for User, Order and Product

from sqlalchemy import ForeignKey, Table, String, Column, DateTime, Float, Integer
from sqlaclhemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

# The association table between Orders and Products
order_product = Table(
    'order_product'
    Base.metadata,
    Column("order_id", ForeignKey("order.id"))
    Column("product_id", ForeignKey("product.id"), unique = True) # no duplicates
)

# Users table 
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200), unique = True)

    # One to Many relationship from User to Order
    orders: Mapped[List["Order"]] = relationship('Order', back_populates = 'user')

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    order_date: Mapped[DateTime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    # Many to One relatinship from Order to User
    user: Mapped[User] = relationship("User", back_populates = 'orders')

    # Many to Many relationship between Order and Product (association/junction table connection)
    products: Mapped[List['Product']] = relationship('Product', secondary = order_product,
        back_populates = 'orders')

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    product_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)

    # Many to Many relationship between Product and Order
    orders: Mapped[List["Order"]] = relationship('Order', secondary = order_product,
        back_populates = "products")