from sqlalchemy import create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHAMY_BATABASE_URL ='sqlite:///../blog.db'

engine = create_engine(SQLALCHAMY_BATABASE_URL, connect_args={"check_same_thread":False})

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
