from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlapp.Models.models import User,Order
from sqlapp.Schemas.schemas import UserCreate, UserUpdate
from fastapi import HTTPException as HE, Response, status
from sqlalchemy import or_

def get_count_users(db: Session):
    return db.query(func.count(User.id)).scalar()


def is_unique(db: Session, sub: str):
    user = db.query(User).filter(or_(User.email ==sub , User.username==sub)).first()
    return user is None


def create_user(db: Session, user: UserCreate):
    new_user = User(**user.dict())
    if not is_unique(db, new_user.email) or not is_unique(db, new_user.username):
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom d'utilisateur ou l'email existe déjà",
        )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HE(status_code=500, detail=f"Erreur lors de la creation de l'utilisateur : {str(e.detail)}")
    return new_user


def get_user(db: Session,id:int = None,  sub: str = None):
    user = db.query(User).filter(or_(User.username == sub , User.email == sub , User.id==id)).first()
    if not user:
        raise HE(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur Non Trouvé")
    else:
        return user


def get_users(db: Session, skip: int = 0, limit: int = None):
    count = get_count_users(db)
    users = db.query(User).offset(skip).limit(limit).all()
    if not users:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aucun utilisateur trouvé"
        )
    else:
        return users

def get_user_orders(db:Session,user_id:int):
    user = get_user(db, user_id)
    return db.query(Order).filter(Order.user_id == user_id).all()


def delete_user(db: Session, user_id):
    user = get_user(db, user_id)
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=500,
            detail=f"Erreur lors de la suppression de l'utilisateur {str(e)}",
        )
    return Response(status_code=200, content={"message": "Utilisateur supprimé avec succès"})


def update_user(db: Session, user_id: int, user: UserUpdate):
    existing_user = get_user(db, user_id)
    try:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(existing_user, key, value)
        db.commit()
        db.refresh(existing_user)
    except HE as e :
        db.rollback()
        raise HE(status_code=500,detail=f"Erreur lors de la mise à jour de l'utilisateur : {str(e.detail)}")
    return existing_user
