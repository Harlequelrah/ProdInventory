from sqlalchemy.orm import Session
from Models.models import Order
from Schemas.schemas import OrderCreate, OrderUpdate, Oder
from fastapi import HTTPException as HE, Response, status, Depends
from Database.database import get_db
from sqlalchemy.sql import func
from harlequelrah_fastapi.entity.utils import update_entity


async def count_orders(db: Session):
    return db.query(func.count(Order.id)).scalar()


async def get_orders(db: Session, skip: int = 0, limit: int = None):
    return db.query(Order).offset(skip).limit(limit).all()


async def get_order(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HE(status_code=status.HTTP_404_NOT_FOUND, detail="Commande Non Trouvée")
    return order


async def create_order(order: OrderCreate, db: Session):
    new_order = Order(**order.dictt)
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création de la commande : {str(e)}",
        )
    return new_order


async def delete_order(order_id: int, db: Session):
    order = await get_order(order_id,db)
    try:
        db.delete()
        db.commit()
        return Response(
        status_code=200, content={"message": "Utilisateur supprimé avec succès"}
    )
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression de la commande : {str(e)}",
        )


async def update_order(order_id: int, order: OrderUpdate, db: Session):
    existing_order = await get_order(order_id,db)
    try:
        update_entity(existing_order, order)
        db.commit()
        db.refresh(existing_order)
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la mise à jour de la commande : {str(e)}",
        )
    return order
