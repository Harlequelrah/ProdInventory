from pydantic import BaseModel,Field
from typing import List,Optional
from datetime import datetime
from decimal import Decimal


class UserBase(BaseModel):
    email:str=Field(example="user@example.com")
    username:str=Field(example="Harlequelrah")
    lastname:str=Field(example="SMITH")
    firstname:str=Field(example="jean-francois")
    date_created:str=Field(example="")

class UserCreate(UserBase):
    password:str=Field(example="m*td*pa**e")

class UserUpdate(BaseModel):
    email:Optional[str]=Field(default=None,example="user@example.com")
    username:Optional[str]=Field(default=None,example="Harlequelrah")
    lastname:Optional[str]=Field(default=None,example="SMITH")
    firstname:Optional[str]=Field(default=None,example="jean-francois")
    password: str = Field(default=None,example="m*td*pa**e")

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
