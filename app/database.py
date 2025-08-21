# yeah database ky sath connection banata hai
from sqlalchemy import create_engine
# ORM ke liye base class banata hai jisse aap apne database tables ko Python classes ki tarah define kar sako.
from sqlalchemy.ext.declarative import declarative_base
# sessions banata hai jisme aap queries chala sakte ho (add, delete, update, select).
from sqlalchemy.orm import sessionmaker


# This the postgres database url connection
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:090078601%40Ab@localhost:5432/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
