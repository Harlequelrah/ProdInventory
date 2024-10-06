from fastapi import APIRouter,Depends
from sqlapp.Database.database import get_db
from sqlalchemy.orm import Session
from sqlapp.Cruds import userCRUD as crud
from sqlapp.Authentication.authenticate import get_current_user
from typing import List
from sqlapp.Schemas.schemas import User, UserCreate,UserUpdate

app_user=APIRouter(
    prefix="/users",
    tags=['users'],
    responses={404: {"description": "Utilisateur non trouvé"}}
)

@app_user.get("/count-users")
async def count_users(db:Session=Depends(get_db)):
    return await crud.get_count_users(db)


@app_user.get('/get-user/{credential}',response_model=User)
async def get_user(credential:str ,db:Session=Depends(get_db),access_token:str=Depends(get_current_user)):
    if credential.isdigit(): return await crud.get_user(id=credential)
    return await crud.get_user(sub=credential,db=db)


@app_user.get('/get-users',response_model=List[User])
async def get_users(
    access_token: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    return await crud.get_users(db)


@app_user.post('/create-user',response_model=User)
async def create_user(user: UserCreate, db:Session=Depends(get_db),access_token: str = Depends(get_current_user)):
    return await crud.create_user(user,db)


@app_user.delete('/delete-user/{id}')
async def delete_user(id: int, db:Session=Depends(get_db),access_token: str = Depends(get_current_user)):
    return await crud.delete_user(id,db)


@app_user.put('/update-user/{id}',response_model=User)
async def update_user(
    user: UserUpdate, id: int,db:Session=Depends(get_db), access_token: str = Depends(get_current_user)
):
    return await crud.update_user(id,user,db)


@app_user.get('/current-user',response_model=User)
async def get_current_user(access_token:str=Depends(get_current_user)):
    return access_token
