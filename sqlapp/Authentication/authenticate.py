from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlapp.Database.database import get_db
from sqlapp.Models.models import User
from sqlapp.Schemas.schemas import AccessToken, RefreshToken
from datetime import datetime, timedelta
from secret import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
CREDENTIALS_EXCEPTION  = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def authenticate_user(db: Session, username_or_email: str, password: str):
    user = (
        db.query(User)
        .filter(User.username == username_or_email | User.email == username_or_email)
        .first()
    )
    if not user or not user.check_password(password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> AccessToken:
    to_encode = data.copy
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnoww() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encode_jwt, "token_type": "bearer"}


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> RefreshToken:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"refresh_token": encode_jwt}


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise CREDENTIALS_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = db.query(User).filter(User.username == sub | User.email == sub).first()
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


def refresh_token(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        sub=payload.get("sub")
        if sub is None : raise CREDENTIALS_EXCEPTION
        user=db.query(User).filter(User.username==sub | User.email==sub).first()
        if user is None: raise CREDENTIALS_EXCEPTION
        access_token_expires=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token=create_access_token(
            data={"sub":sub},expires_delta=access_token_expires
        )
        return access_token
    except JWTError:
        raise CREDENTIALS_EXCEPTION
