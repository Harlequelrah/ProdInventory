from sqlalchemy.orm import Session
from sqlapp.Schemas.schemas import (
    Order_Product,
    Order_ProductCreate,
    Order_ProductUpdate,
)
from sqlapp.Database.database import get_db
from sqlapp.Authentication.authenticate import get_current_user
import sqlapp.Cruds.order_productCRUD as crud
from fastapi import Depends, APIRouter
from typing import List


app_order_product = APIRouter(prefix="/order_products", tags=["order_products"])


@app_order_product.post("/create-order-product", response_model=Order_Product)
async def create_order_product(
    order_product: Order_ProductCreate,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    return await crud.create_order_product(order_product,db)


@app_order_product.get(
    "/get-order-product-by/order/{order_id}/product/{product_id}",
    response_model=Order_Product,
)
async def get_order_product(
    order_id: int,
    product_id: int,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    return await crud.get_order_product(order_id, product_id, db)


@app_order_product.get("/get-order-products", response_model=List[Order_Product])
async def get_order_products(
    db: Session = Depends(get_db), access_token: str = Depends(get_current_user)
):
    return await crud.get_order_products(db)


@app_order_product.get(
    "/get-order-products/by-order/{order_id}", response_model=List[Order_Product]
)
async def get_order_products_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    return await crud.get_order_products_by_order(order_id, db)


@app_order_product.get(
    "/get-order-products/by-product/{product_id}", response_model=List[Order_Product]
)
async def get_order_products_by_order(
    product_id: int,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    return await crud.get_order_products_by_product(product_id, db)


@app_order_product.put("/update-order_product/by/order/{order_id}/product/{product_id}",response_model=Order_Product)
async def update_order_product(order_id:int,product_id:int,order_product:Order_ProductUpdate,db:Session=Depends(get_db),acces_token:str=Depends(get_current_user)):
    return await crud.update_order_product(order_id,product_id,order_product,db)

@app_order_product.delete("/delete-order-product/by/order/{order_id}/product/{product_id}")
async def delete_order_product(order_id:int,product_id:int,db:Session=Depends(get_db),acces_token:str=Depends(get_current_user)):
    return await crud.delete_order_product(order_id,product_id,db)
