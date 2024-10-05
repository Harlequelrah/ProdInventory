from sqlalchemy.sql import func
from fastapi import HTTPException, status, Depends,Response
from sqlapp.Models.models import Category
from sqlapp.Schemas.schemas import CategoryCreate, CategoryUpdate
from sqlalchemy.orm import Session
from sqlapp.Database.database import get_db
from harlequelrah_fastapi.entity.utils import update_entity


async def get_count_categories(db: Session):
    return db.query(func.count(Category.id)).scalar()


async def create_category(category: CategoryCreate, db: Session):
    new_category = Category(**category.dict())
    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Erreur lors de la création de la categorie",
        )
    return new_category


async def get_category(category_id: int, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP__404__NOT_FOUND, detail="Categorie Non Trouvée"
        )
    return category


async def get_categories(db: Session, skip: int = 0, limit: int = None):
    limit = await get_count_categories(db)
    categories = db.query(Category).offset(skip).limit(limit).all()
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aucune categorie trouvée"
        )
    return categories


async def delete_category(category_id: int, db: Session):
    category = await get_category(category_id, db)
    try:
        db.delete(category)
        db.commit()
        return Response(
        status_code=204, content={"message": "Utilisateur supprimé avec succès"}
    )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la suppresion de la categorie {str(e)}"
        )


async def update_category(category_id, category: CategoryUpdate, db: Session):
    existing_category = await  get_category(category_id, db)
    try:
        update_entity(existing_category, category)
        db.commit()
        db.refresh(existing_category)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour de la categorie : {str(e)}",
        )
    return existing_category
