from pydantic import BaseModel,Field
from typing import List,Optional
from datetime import datetime
from decimal import Decimal
from sqlapp.Authentication.secret import SECRET_KEY

class UserBase(BaseModel):
    email:str=Field(example="user@example.com")
    username:str=Field(example="Harlequelrah")
    lastname:str=Field(example="SMITH")
    firstname:str=Field(example="jean-francois")

class UserCreate(UserBase):
    password:str=Field(example="m*td*pa**e")

class UserUpdate(BaseModel):
    email:Optional[str]=None
    username:Optional[str]=None
    lastname:Optional[str]=None
    firstname:Optional[str]=None
    is_active:Optional[bool]=None
    password: Optional[str]=None
    orders: Optional[List["Order"]]=[]

class User(UserBase):
    id:int
    is_active:bool
    date_created:datetime
    orders:List["Order"]=[]

    class config :
        from_orm=True


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    refresh_token :str
    token_type:str

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

class ProductBase(BaseModel):
    name:str=Field(example="table")
    description:str=Field(example="Grande table pour le salon")
    price:Decimal = Field(example=50.75)


class ProductCreate(ProductBase):
    quantity_available: int = Field(example=25)

class ProductUpdate(BaseModel):
    name:Optional[str]=None
    description:Optional[str]=None
    price:Optional[Decimal]=None
    quantity_available:Optional[int]=None
    orders: Optional[List["Order"]]=[]
    category_id:Optional[int]=None

class Product(ProductCreate):
    id:int
    orders:List["Order"]
    category_id:int
    class Config:
        from_orm=True


class OrderBase(BaseModel):
    user_id:int=Field(example=69)
    products:List[int]

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    user_id:Optional[int]=None
    products:Optional[List[int]]=[]


class Order(OrderBase):
    id:int
    order_date:datetime
    class config:
        from_orm=True


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


# class UserLogin(BaseModel):
#     username: str
#     password: str
