from sqlalchemy.sql import func
from fastapi import HTTPException, status
from Models.models import Category
from Schemas.schemas import CategoryCreate, CategoryUpdate, Category
from sqlalchemy.orm import Session


def get_count_categories(db:Session):
    return db.query(func.count(Category.id)).scalar()


def create_category(db: Session, category: CategoryCreate):
    new_category = Category(**category.dict())
    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except Exception as e :
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Erreur lors de la création de la categorie")
    return new_category


def get_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None : raise HTTPException(status_code=status.HTTP__404__NOT_FOUND,detail="Categorie Non Trouvée")
    return category

def get_categories(db:Session,skip:int=0,limit:int=None):
    limit=get_count_categories(db)
    categories=db.query(Category).offset(skip).limit(limit).all()
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aucune categorie trouvée"
        )
    return categories


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    try:
        db.delete(category)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Erreur lors de la suppresion de la categorie"
        )


def update_category(db: Session, category_id,category:CategoryUpdate):
    existing_category = get_category(db, category_id)
    try:
        for key , value in category.dict(exclude_unset=True).items():
            setattr(existing_category,key,value)
        db.commit()
        db.refresh(update_category)
    except Exception as e :
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Erreur lors de la mise à jour de la categorie : {str(e.errors)}")
    return existing_category
