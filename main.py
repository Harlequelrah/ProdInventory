from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from sqlapp.Models import models
from sqlapp.Schemas.schemas import AccessToken, Token, User,UserLoginModel
from sqlapp.Database.database import engine, get_db
from sqlapp.Authentication import authenticate,secret
from fastapi.security import OAuth2PasswordRequestForm

from routes.user import app_user
from routes.category import app_category
from routes.product import app_product
from routes.order_product import app_order_product
from routes.order import app_order


app = FastAPI()
app.include_router(app_user)
app.include_router(app_category)
app.include_router(app_product)
app.include_router(app_order)
app.include_router(app_order_product)

models.Base.metadata.create_all(bind=engine)

AUTHENTICATION_EXCEPTION=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/username or password",
            headers={"WWW-Authenticate": "Beaer"},
        )

@app.post("/token", response_model=Token)
async def login_api_user(
    form_data: OAuth2PasswordRequestForm =Depends(), db: Session = Depends(get_db)
):
    user = await authenticate.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/username or password",
            headers={"WWW-Authenticate": "Beaer"},
        )
    data = {"sub": form_data.username}
    access_token = authenticate.create_access_token(data)
    refresh_token = authenticate.create_refresh_token(data)

    return {'access_token': access_token['access_token'],'refresh_token': refresh_token['refresh_token'],'token_type':'bearer'}


@app.get("/refresh-token", response_model=AccessToken)
async def refresh_token(current_user: User = Depends(authenticate.get_current_user)):
    data = {"sub": current_user.username}
    access_token = authenticate.create_access_token(data)
    return access_token

@app.post("/login",response_model=Token)
async def login(usermodel:UserLoginModel,db:Session=Depends(get_db)):
    if (usermodel.email is None ) ^ (usermodel.username is None):
        credential = usermodel.username if usermodel.username  else usermodel.email
        user = await authenticate.authenticate_user(
        db, credential, usermodel.password
    )
        if not user: raise AUTHENTICATION_EXCEPTION
        data = {"sub": credential}
        access_token = authenticate.create_access_token(data)
        refresh_token = authenticate.create_refresh_token(data)
        return {'access_token': access_token['access_token'],'refresh_token': refresh_token['refresh_token'],'token_type':'bearer'}
    else :raise AUTHENTICATION_EXCEPTION


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
