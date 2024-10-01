from fastapi import APIRouter,Depends
from sqlapp.Database.database import get_db
from sqlalchemy.orm import Session
from sqlapp.Cruds import userCRUD as crud
from sqlapp.Authentication import authenticate
from typing import List
from sqlapp.Schemas.schemas import UserCreate,UserUpdate,User

app_user=APIRouter(
    prefix="/users",
    tags=['users'],
    responses={404: {"description": "Utilisateur non trouvé"}}
)

@app_user.get('/get-user/{credential}',response_model=User)
async def get_user(credential:str ,db:Session=Depends(get_db)):
    if credential.isdigit(): return crud.get_user(db,id=credential)
    return crud.get_user(db,sub=credential)

@app_user.get('/get-users',response_model=List[User])
async def get_users(db:Session=Depends(get_db)):
    return crud.get_users(db)

@app_user.post('/create-user',response_model=User)
async def create_user(user:UserCreate,db:Session=Depends(get_db)):
    return crud.create_user(db,user)

@app_user.delete('/delete-user/{id}')
async def delete_user(id:int,db:Session=Depends(get_db)):
    return crud.delete_user(db,id)

@app_user.put('/update-user/{id}',response_model=User)
async def update_user(user:UserUpdate,id:int,db:Session=Depends(get_db)):
    return crud.update_user(db,id,user)

@app_user.get('/current-user',response_model=User)
async def get_current_user(refresh_token:str=Depends(authenticate.get_current_user)):
    return refresh_token
