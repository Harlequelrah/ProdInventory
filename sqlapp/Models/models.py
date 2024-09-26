from sqlalchemy import Column , DECIMAL , Integer , String ,DateTime ,ForeignKey
from sqlapp.Database.database import Base
import bcrypt # type: ignore
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    email = Column(String(256),unique=True,index=True)
    username = Column(String(256),unique=True,index=True)
    password=Column(String(256))
    def set_password (self,password:str):
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password:str) -> bool:
        if bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8')):return True
        else:return False

class Category(Base):
    __tablename__='categories'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(256),unique=True,index=True)
    label=Column(String(256), nullable=False)

class Product(Base):
    __tablename__='products'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(256),unique=True,index=True)
    description = Column(String(256),nullable=False)
    price=Column(DECIMAL(10,2))
    date_created=Column(DateTime,nullable=False,default=func.now())
    date_updated=Column(DateTime,nullable=True,onupdate=func.now())
    category_id=Column(Integer,ForeignKey('categories.id'),nullable=False)
    category=relationship('Category')



