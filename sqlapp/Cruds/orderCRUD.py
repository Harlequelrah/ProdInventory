from sqlalchemy.orm import Session
from Models.models import Order
from Schemas.schemas import OrderCreate,OrderUpdate,Oder
from fastapi import HTTPException as HE , status
from sqlalchemy.sql import func


def count_orders(db:Session):
    return db.query(func.count(Order.id)).scalar()


def get_orders(db:Session,skip:int=0,limit:int=None):
    return db.query(Order).offset(skip).limit(limit).all()

def get_order(db:Session, order_id:int):
    order= db.query(Order).filter(Order.id==order_id).first()
    if not order :raise HE(status_code=status.HTTP_404_NOT_FOUND,detail="Commande Non Trouvée")
    return order

def create_order(db:Session,order:OrderCreate):
    new_order=Order(**order.dictt)
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except Exception as e :
        db.rollback()
        raise HE(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Erreur lors de la création de la commande : {str(e.detail)}")
    return new_order

def delete_order(db:Session,order_id:int):
    order=get_order(db,order_id)
    try:
        db.delete()
        db.commit()
    except Exception as e :
        db.rollback()
        raise HE(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Erreur lors de la suppression de la commande : {str(e.detail)}")

def update_order(db:Session, order_id:int, order:OrderUpdate):
    existing_order=get_order(db,order_id)
    try:
        for key,value in order.dict(exclude_unset=True).items():
            setattr(existing_order,key,value)
        db.commit()
    except Exception as e :
        db.rollback()
        raise HE(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Erreur lors de la mise à jour de la commande : {str(e.detail)}")
    return order
