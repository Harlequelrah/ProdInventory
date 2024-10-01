from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from Models.models import Product
from Schemas.schemas import ProductCreate , ProductUpdate , Product
from fastapi import HTTPException as HE,status
from harlequelrah_fastapi.entity.utils import update_entity

def count_products(db:Session):
    return db.query(func.count(Product)).scalar()

def get_product(db:Session,product_id):
    product=db.query(Product).filter(Product.id==product_id).first()
    if not product : raise HE(status_code=status.HTTP_404_NOT_FOUND,detail="Le produit n'a pas été trouvé")
    return product


def get_products_by_category(db: Session, category_id):
    product = db.query(Product).filter(Product.category_id == category_id).all()
    if not product:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun produit n'a pas été trouvé pour cette catégorie"
        )
    return product


def get_products(db:Session,skip:int=0, limit:int=None):
    products= db.query(Product).offset(skip).limit(limit).all()
    if not products : raise HE(status_code=status.HTTP_404_NOT_FOUND,detail="Aucun produit n'a pas été trouvé")
    return products

def create_product(db:Session,product:ProductCreate):
    new_product=Product(**product)
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except Exception as e:
        raise HE(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Erreur lors de la création du produit : {str(e.detail)}")

def delete_product(db:Session,product_id:int):
    product=get_product(db,product_id)
    try:
        db.delete(product)
        db.commit()
    except  Exception as e:
        db.rollback()
        raise HE(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Erreur lors de la suppression du produit : {str(e.detail)}")

def update_product(db:Session,product_id:int,product:ProductUpdate):
    existing_product=get_product(db,product_id)
    try:
        update_entity(existing_product,product)
        db.commit()
        db.refresh(existing_product)
    except Exception as e:
        db.rollback()
        raise HE(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Erreur lors de la modification du produit : {str(e.detail)}")


def update_product_quantiy(db: Session, product_id: int,quantity:int):
    existing_product = get_product(db, product_id)
    try:
        existing_product.update_quantity_available(quantity=quantity)
        db.commit()
        db.refresh(existing_product)
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la modification du produit : {str(e.detail)}",
        )
