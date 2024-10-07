from sqlalchemy.orm import Session
from sqlapp.Models.models import Order, Product, Order_Product
from sqlapp.Schemas.schemas import Order_ProductCreate, OrderCreate, OrderUpdate
from fastapi import HTTPException as HE, Response, status, Depends
from sqlapp.Database.database import get_db
from sqlalchemy.sql import func
from sqlapp.Cruds.productCRUD import get_product
from sqlapp.Cruds.userCRUD import get_user
from sqlapp.Cruds import order_productCRUD as O_Pcrud
from harlequelrah_fastapi.utility.utils import update_entity


async def count_orders(db: Session):
    return db.query(func.count(Order.id)).scalar()


async def get_orders(db: Session, skip: int = 0, limit: int = None):
    return db.query(Order).offset(skip).limit(limit).all()


async def get_orders_by_user(user_id: int, db: Session):
    return db.query(Order).filter(Order.user_id == user_id).all()


async def get_order(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HE(status_code=status.HTTP_404_NOT_FOUND, detail="Commande Non Trouvée")
    return order


async def create_order(order: OrderCreate, db: Session):
    new_order = Order(user_id=order.user_id,order_products=[])
    try:
        user = await get_user(db, order.user_id)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        for product in order.products:
            new_order_product=Order_ProductCreate(
                product_id=product.product_id,
                product_amount=product.product_amount,
                order_id=new_order.id,
            )
            await O_Pcrud.create_order_product(new_order_product,db)
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création de la commande : {str(e)}",
        )
    return new_order


async def delete_order(order_id: int, db: Session):
    try:
        order = await get_order(order_id, db)
        for order_product in order.order_products:
            order_product.product.update_quantity_available(order_product.product_amount)
        db.delete(order)
        db.commit()
        return Response(status_code=200, content="Commande supprimée avec succès")
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression de la commande : {str(e)}",
        )


async def update_order(order_id: int, order: OrderUpdate, db: Session):
    existing_order = await get_order(order_id, db)
    try:
        user = await get_user(db, order.user_id)
        for order_product in order.products:
            existing_order_product=await O_Pcrud.get_order_product(order_id,order_product.product_id,db)
            delta = existing_order_product.product_amount - order_product.product_amount
            update_entity(existing_order_product, order_product)
            if delta > 0 :
                existing_order_product.product.update_quantity_available(delta)
            elif delta< 0 :
                existing_order_product.product.order_product(-delta)
        db.commit()
        db.refresh(existing_order)
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la mise à jour de la commande : {str(e)}",
        )
    return existing_order
