from pydantic import BaseModel,Field
from typing import List,Optional
from datetime import datetime
from decimal import Decimal
from fastapi import Form
from sqlapp.Authentication.secret import SECRET_KEY


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserBaseModel(BaseModel):
    email:str=Field(example="user@example.com")
    username:str=Field(example="Harlequelrah")
    lastname:str=Field(example="SMITH")
    firstname:str=Field(example="jean-françois")

class UserCreate(UserBaseModel):
    password:str=Field(example="m*td*pa**e")

class UserUpdate(BaseModel):
    email:Optional[str]=None
    username:Optional[str]=None
    lastname:Optional[str]=None
    firstname:Optional[str]=None
    is_active:Optional[bool]=None
    password: Optional[str]=None

class UserBase(UserBaseModel):
    id:int
    is_active:bool
    date_created:datetime
    class config :
        from_orm=True

class FullUser(UserBase):
    user_orders: List["Order"] = []

class User(UserBase):
    user_orders:List["MetaOrder"]=[]


class CategoryBase(BaseModel):
    name:str=Field(example="vêtement")
    label:str=Field(example="habits en tout genre et pour tout âge")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name:Optional[str]=None
    label: Optional[str] = None

class Category(CategoryBase):
    id:int
    class config:
        from_orm =True

class ProductBaseModel(BaseModel):
    name:str=Field(example="table")
    description:str=Field(example="Grande table pour le salon")
    price:Decimal = Field(example=50.75)
    quantity_available: int = Field(example=25)


class ProductCreate(ProductBaseModel):
    category_id:int

class ProductUpdate(BaseModel):
    name:Optional[str]=None
    description:Optional[str]=None
    price:Optional[Decimal]=None
    quantity_available:Optional[int]=None
    category_id:Optional[int]=None

class ProductBase(ProductBaseModel):
    id:int
    category_id:int
    class Config:
        from_orm=True

class FullProduct(ProductBase):
    product_orders: List["Order_Product"]

class Product(ProductBase):
    product_orders:List["OrderProduct_Order"]


class OrderProduct_Product(BaseModel):
    product_id:int
    product_amount:int

class OrderProduct_Order(BaseModel):
    order_id:int
    product_amount:int

class OrderBase(BaseModel):
    user_id:int=Field(example=69)


class OrderCreate(OrderBase):
    products:List[OrderProduct_Product]


class OrderUpdate(BaseModel):
    user_id:Optional[int]=Field(default=None,example=1)
    products:Optional[List[OrderProduct_Product]]=[]


class Order(BaseModel):
    id:int
    user_id: int = Field(example=69)
    order_date:datetime
    order_products: List["OrderProduct_Product"] = []
    class config:
        from_orm=True

class MetaOrder(BaseModel):
    id:int
    order_date:datetime


class Order_ProductBase(BaseModel):
    product_amount:int=Field(example=35)

class Order_ProductCreate(Order_ProductBase):
    order_id:int=Field(example=5)
    product_id:int=Field(example=3)

class Order_ProductUpdate(BaseModel):
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    product_amount: Optional[int] = None

class Order_Product(Order_ProductBase):
    order_id:int
    product_id:int
    class Config:
        from_orm=True

class UserLoginModel(BaseModel):
    username: Optional[str]=None
    password: str
    email:Optional[str]=None
