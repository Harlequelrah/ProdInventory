from sqlalchemy import Column, DECIMAL, Integer, String, DateTime, ForeignKey
from sqlapp.Database.database import Base
import bcrypt  # type: ignore
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(256), unique=True, index=True)
    password = Column(String(256))
    orders = relationship("Order", back_populates="user")

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        if bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8")):
            return True
        else:
            return False


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True, index=True)
    label = Column(String(256), nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True, index=True)
    description = Column(String(256), nullable=False)
    price = Column(DECIMAL(10, 2))
    date_created = Column(DateTime, nullable=False, default=func.now())
    date_updated = Column(DateTime, nullable=True, onupdate=func.now())
    quantity_available = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category")
    orders = relationship(
        "Order", secondary="order_products", back_populates="products"
    )

    def can_be_ordered(self, orderer_quantity: int):
        if self.quantity_available - orderer_quantity >= 0:
            return True
        else:
            return False


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    products = relationship("Order_Product", back_populates="order")
    order_amount = Column(DECIMAL(10, 2))
    order_date = Column(DateTime, default=func.now())


    def update_order_amount(self):
        total_amount = 0
        for ordered_product in self.products:
            if ordered_product.product.can_be_ordered(ordered_product.product_amount):
                total_amount += (
                    ordered_product.product_amount * ordered_product.product.price
                )
                ordered_product.product.quantity_available -= ordered_product.product_amount
            else:
                raise ValueError(
                    f"Quantité demandée pour le produit {ordered_product.product.name} non disponible."
                )

        self.order_amount = total_amount


class Order_Product(Base):
    __tablename__ = "order_products"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    product = relationship("Product")
    order = relationship("Order", back_populates="products")
    product_amount = Column(Integer)
