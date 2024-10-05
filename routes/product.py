from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from sqlapp.Authentication.authenticate import get_current_user
from sqlapp.Database.database import get_db
from sqlapp.Schemas.schemas import Product,ProductCreate,ProductUpdate,Category
from typing import List
from sqlapp.Cruds import productCRUD as crud

app_product=APIRouter(
    prefix='/products',
    tags=['products'],
)
@app_product.get("/count-products")
async def count_products(db:Session=Depends(get_db)):
    return await crud.count_products(db)

@app_product.get("/get-products",response_model=List[Product])
async def get_products(db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.get_products(db)


@app_product.get("/get-products/by/category/{category_id}", response_model=List[Product])
async def get_products_by_category(category_id:int,
    db: Session = Depends(get_db), access_token: str = Depends(get_current_user)
):
    return await crud.get_products_by_category(category_id,db)


@app_product.get("/get-product/{product_id}",response_model=Product)
async def get_product(product_id:int,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.get_product(product_id,db)

@app_product.post("/create-product",response_model=Product)
async def create_product(product:ProductCreate,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.create_product(product,db)

@app_product.delete("/delete-product/{product_id}")
async def delete_product(product_id:int,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.delete_product(product_id,db)

@app_product.put("/update-product/{product_id}",response_model=Product)
async def update_product(product_id:int,product:ProductUpdate,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.update_product(product_id,product,db)

@app_product.put("/update-product-quantity/{product_id}")
async def update_product_quantity(product_id:int,quantity:int,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.update_product_quantity(product_id,quantity,db)
