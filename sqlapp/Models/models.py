from sqlalchemy import (
    Boolean,
    Column,
    DECIMAL,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
)
from sqlapp.Database.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from argon2 import PasswordHasher, exceptions as Ex


Ph = PasswordHasher()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(256), unique=True, index=True)
    password = Column(String(1024))
    lastname = Column(String(256), nullable=False)
    firstname = Column(String(256), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    is_active = Column(Boolean, default=True)
    user_orders = relationship("Order", back_populates="user")

    def set_password(self, password: str):
        self.password = Ph.hash(password)
        return self.password

    def check_password(self, password: str) -> bool:
        try:
            Ph.verify(self.password, password)
            return True
        except Ex.VerifyMismatchError:
            return False
        except Ex.InvalidHashError:
            self.set_password(password)
            return self.check_password(password)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True, index=True)
    label = Column(String(256), nullable=False)
    products=relationship("Product",back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True, index=True)
    description = Column(String(256), nullable=False)
    price = Column(DECIMAL(10, 2))
    date_created = Column(DateTime, nullable=False, default=func.now())
    date_updated = Column(DateTime, nullable=True, onupdate=func.now())
    quantity_available = Column(Integer, default=None)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category",back_populates="products")
    product_orders = relationship("Order_Product", back_populates="product")

    def can_be_ordered(self, orderer_quantity: int):
        if orderer_quantity <= 0:
            raise ValueError("La quantité doit être positive et non nulle")
        return self.quantity_available >= orderer_quantity

    def update_quantity_available(self, quantity: int):
        if quantity <= 0:
            raise ValueError("La quantité doit être positive et non nulle")
        self.quantity_available += quantity

    def order(self, quantity: int):
        if quantity <= 0:
            raise ValueError("La quantité doit être positive et non nulle")
        self.quantity_available -= quantity


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_orders")
    order_products = relationship("Order_Product", back_populates="order")
    order_date = Column(DateTime, default=func.now())

    def get_order_amount(self):
        total_amount = 0
        for ordered_product in self.products:
            if ordered_product.product.can_be_ordered(ordered_product.product_amount):
                total_amount += (
                    ordered_product.product_amount * ordered_product.product.price
                )
                ordered_product.product.quantity_available -= (
                    ordered_product.product_amount
                )
            else:
                raise ValueError(
                    f"Quantité demandée pour le produit {ordered_product.product.name} non disponible."
                )

        return total_amount


class Order_Product(Base):
    __tablename__ = "order_products"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    product = relationship("Product",back_populates="product_orders")
    order = relationship("Order",back_populates="order_products")
    product_amount = Column(Integer)
