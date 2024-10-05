from fastapi import APIRouter,Depends
from sqlapp.Database.database import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlapp.Authentication.authenticate import get_current_user
from sqlapp.Schemas.schemas import Category,CategoryCreate,CategoryUpdate
from sqlapp.Cruds import categoryCRUD as crud

app_category=APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@app_category.get("/count-categories")
async def count_categories(db: Session = Depends(get_db)):
    return await crud.get_count_categories(db)


@app_category.get("/get-categories",response_model=List[Category])
async def get_categories(db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.get_categories(db)

@app_category.get("/get-category/{category_id}",response_model=Category)
async def get_category(category_id:int,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.get_category(category_id,db)

@app_category.post("/create-category",response_model=Category)
async def create_category(category:CategoryCreate,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.create_category(category,db)

@app_category.put("/update-category/{category_id}",response_model=Category)
async def update_category(category_id:int,category:CategoryUpdate,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.update_category(category_id,category,db)

@app_category.delete("/delete-category/{category_id}")
async def delete_category(category_id:int,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    return await crud.delete_category(category_id,db)
