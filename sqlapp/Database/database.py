from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from FASTAPI.ProdInventory.sqlapp.Authentication.secret import username , password

SQLALCHEMY_DATABASE_URL=f"mysql+mysqlconnector://{username}:{password}@localhost:3306/prodinventory"
engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)
sessionLocal=sessionmaker(autocomit=False,autoflush=False,bind=engine)
Base=declarative_base()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
