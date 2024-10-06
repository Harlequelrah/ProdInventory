from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE, Response, status, Depends
from sqlapp.Database.database import get_db
from sqlapp.Models.models import Order_Product
from sqlapp.Schemas.schemas import  Order_ProductCreate, Order_ProductUpdate
from harlequelrah_fastapi.entity.utils import update_entity
from sqlalchemy import and_
from typing import Optional
from . import productCRUD as Pcrud


async def get_count_order_product(db: Session):
    return db.query(func.count()).select_from(Order_Product).scalar()

async def get_order_products(db:Session):
    order_products= db.query(Order_Product).all()
    if not order_products: raise HE(status_code=status.HTTP_404_NOT_FOUND,detail="Aucune Commande-Produit n'a été trouvée")
    return order_products



async def get_order_product(
    order_id: int, product_id: int, db : Session
):
    order_product = (
        db.query(Order_Product)
        .filter(
            and_(
                Order_Product.order_id == order_id,
                Order_Product.product_id == product_id,
            )
        )
        .first()
    )
    if not order_product:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commande-Produit non trouvée"
        )
    return order_product


async def get_order_products_by_order(order_id: int,db:Session):
    order_products = (
        db.query(Order_Product).filter(Order_Product.order_id == order_id).all()
    )
    if not order_products:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune commande-produit n'a été retrouvée pour cette commande",
        )
    return order_products


async def get_order_products_by_product(product_id: int, db : Session):
    order_products = (
        db.query(Order_Product).filter(Order_Product.product_id == product_id).all()
    )
    if not order_products:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune commande-produit n'a été retrouvée pour ce produit",
        )
    return order_products


async def create_order_product(
    order_product: Order_ProductCreate, db : Session
):
    new_order_product = Order_Product(**order_product.dict())
    try:
        db.add(new_order_product)
        db.commit()
        db.refresh(new_order_product)
        await Pcrud.order_product(order_product.product_id,order_product.product_amount,db)
    except Exception as e:
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erreur lors de la creation d'une ligne de commande produit",
        )
    return new_order_product


async def delete_order_product(order_id: int,product_id:int, db : Session):
    order_product = await get_order_product(order_id, product_id,db)
    try:
        db.delete(order_product)
        db.commit()
        return Response(
        status_code=200, content="Commande-Produit supprimé avec succès"
    )
    except Exception as e:
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erreur lors de la suppression de la ligne de commande produit",
        )



async def update_order_product(
    order_id: int,
    product_id:int,
    order_product: Order_ProductUpdate,
    db : Session,
):
    existing_order_product = await get_order_product(order_id, product_id)
    try:
        update_entity(existing_order_product, order_product)
        db.commit()
        db.refresh(existing_order_product)
    except Exception as e:
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erreur lors de la mise à jour de la ligne de commande produit",
        )
