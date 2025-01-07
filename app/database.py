from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from .config import sql_db_url

SQLALCHEMY_DATABASE_URL = sql_db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
