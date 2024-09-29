from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE , status
from Models.models import Order_Product
from Schemas.schemas import Order_Product,Order_ProductCreate,Order_ProductUpdate
from sqlalchemy import and_
def get_count_order_product(db:Session):
    return db.query(func.count(Order_Product.id)).scalar()

def get_order_product(db:Session,order_id:int,product_id:int):
    order_product=db.query(Order_Product).filter(and_(Order_Product.order_id==order_id,Order_Product.product_id==product_id)).first()
    if not order_product: raise HE(status_code=status.HTTP_404_NOT_FOUND,detail="Commande-Produit non trouvée")
    return order_product

def get_order_product_by_order(db:Session,order_id:int):
    order_products=db.query(Order_Product).filter(Order_Product.order_id==order_id).all()
    if not order_products:raise HE(status_code=status.HTTP_404_NOT_FOUND,detail="Aucune commande-produit n'a été retrouvée pour cette commande")
    return order_products


def get_order_product_by_product(db: Session, product_id: int):
    order_products = (
        db.query(Order_Product).filter(Order_Product.product_id == product_id).all()
    )
    if not order_products:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune commande-produit n'a été retrouvée pour ce produit",
        )
    return order_products

def create_order_product(db:Session,order_product:Order_ProductCreate):
    new_order_product=Order_Product(**order_product.dict())
    try:
        db.add(new_order_product)
        db.commit()
        db.refresh(new_order_product)
    except Exception as e:
        raise HE(status_code=status.HTTP_400_BAD_REQUEST,detail="Erreur lors de la creation d'une ligne de commande produit")
    return new_order_product

def delete_order_product(db:Session,order_product_id:int):
    order_product=get_order_product(db,order_product_id)
    try:
        db.delete(order_product)
        db.commit()
    except Exception as e:
        raise HE(status_code=status.HTTP_400_BAD_REQUEST,detail="Erreur lors de la suppression de la ligne de commande produit")
    return order_product

def update_order_product(db:Session,order_product_id:int,order_product:Order_ProductUpdate):
    existing_order_product=get_order_product(db,order_product_id)
    try:
        for key,value in order_product.dict().items():
            setattr(existing_order_product,key,value)
    except Exception as e:
        raise HE(status_code=status.HTTP_400_BAD_REQUEST,detail="Erreur lors de la mise à jour de la ligne de commande produit")
