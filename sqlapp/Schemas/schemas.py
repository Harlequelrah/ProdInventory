from pydantic import BaseModel,Field
from typing import List,Optional
from datetime import datetime
from decimal import Decimal


class UserBase(BaseModel):
    email:str=Field(example="user@example.com")
    username:str=Field(example="Harlequelrah")
    lastname:str=Field(example="SMITH")
    firstname:str=Field(example="jean-francois")

class UserCreate(UserBase):
    password:str=Field(example="m*td*pa**e")

class UserUpdate(BaseModel):
    email:Optional[str]
    username:Optional[str]
    lastname:Optional[str]
    firstname:Optional[str]
    is_active=Optional[bool]
    password: Optional[str]

class User(UserBase):
    id:int
    is_active:bool
    date_created:datetime
    order:List[int]=[]

    class config :
        from_orm=True


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str


class Tokens(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken

class CategoryBase(BaseModel):
    name:str=Field(example="vêtement")
    label:str=Field(example="habits en tout genre et pour tout âge")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name:Optional[str]
    label:Optional[str]

class Category(CategoryBase):
    id:int
    class config:
        from_orm =True

class ProductBase(BaseModel):
    name:str=Field(example="table")
    description:str=Field(example="Grande table pour le salon")
    price:Decimal = Field(example=50.75)


class ProductCreate(ProductBase):
    quantity_available: int = Field(example=25)

class ProductUpdate(BaseModel):
    name:Optional[str]
    description:Optional[str]
    price:Optional[Decimal]
    quantity_available:Optional[int]

class Product(ProductCreate):
    id:int
    orders:List[int]
    category_id:int
    class Config:
        from_orm=True

class Order(BaseModel):
    id:int
    user_id:int
    products:List[int]
    order_date:datetime
    class config:
        from_orm=True

class Order_ProductBase(BaseModel):
    product_amount:int=Field(example=35)

class Order_ProductCreate(Order_ProductBase):
    pass

class Order_ProductUpdate(BaseModel):
    product_amount: Optional[int] 

class Order_Product(Order_ProductBase):
    order_id:int
    product_id:int
    class Config:
        from_orm=True
