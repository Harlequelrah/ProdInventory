from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlapp.Models.models import Product
from sqlapp.Schemas.schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException as HE, Response, status, Depends
from sqlapp.Database.database import get_db
from harlequelrah_fastapi.entity.utils import update_entity


async def count_products(db: Session):
    return db.query(func.count(Product.id)).scalar()


async def get_product(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Le produit n'a pas été trouvé",
        )
    return product


async def get_products_by_category(category_id: int, db: Session):
    product = db.query(Product).filter(Product.category_id == category_id).all()
    if not product:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun produit n'a pas été trouvé pour cette catégorie",
        )
    return product


async def get_products(db: Session, skip: int = 0, limit: int = None):
    products = db.query(Product).offset(skip).limit(limit).all()
    if not products:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun produit n'a pas été trouvé",
        )
    return products


async def create_product(product:ProductCreate, db: Session):
    new_product = Product(**product.dict())
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except Exception as e:
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création du produit : {str(e)}",
        )
    return new_product


async def delete_product(product_id: int, db: Session):
    product = await get_product(product_id,db)
    try:
        db.delete(product)
        db.commit()
        return Response(
        status_code=204, content="Produit supprimé avec succès"
    )
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression du produit : {str(e)}",
        )


async def update_product(product_id: int, product: ProductUpdate, db: Session):
    existing_product = await get_product(product_id,db)
    try:
        update_entity(existing_product, product)
        db.commit()
        db.refresh(existing_product)
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Erreur lors de la modification du produit : {str(e)}",
        )
    return existing_product


async def update_product_quantiy(product_id: int, quantity: int, db: Session):
    existing_product = get_product(product_id,db)
    try:
        existing_product.update_quantity_available(quantity=quantity)
        db.commit()
        db.refresh(existing_product)
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la modification du produit : {str(e)}",
        )
