from sqlalchemy.orm import Session
from sqlapp.Schemas.schemas import (
    OrderCreate,
    Order,
    OrderUpdate,
)
from sqlapp.Database.database import get_db
from sqlapp.Authentication.authenticate import get_current_user
import sqlapp.Cruds.orderCRUD as crud
from fastapi import Depends, APIRouter
from typing import List

app_order=APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@app_order.get("/get-orders",response_model=List[Order])
async def get_orders(db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.get_orders(db)


@app_order.get("/get-order/{order_id}",response_model=Order)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user)
):
    return await crud.get_order(order_id,db)

@app_order.get("/get-orders-by/user/{user_id}",response_model=List[Order])
async def  get_order_by_user(user_id:int,db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user)):
    return await crud.get_orders_by_user(user_id,db)


@app_order.post("/create-order",response_model=Order)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    return await crud.create_order(order, db)

@app_order.put("/update-order/{order_id}",response_model=Order)
async def update_order(order_id:int,order:OrderUpdate,db:Session=Depends(get_db),acces_token:str=Depends(get_current_user)):
    return await crud.update_order(order_id,order,db)


@app_order.delete("/delete-order/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    acces_token: str = Depends(get_current_user),
):
    return await crud.delete_order(order_id, db)
