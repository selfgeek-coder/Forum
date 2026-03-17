from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import db_url

engine = create_engine(
    db_url, 
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_database():
    """Инициализация базы данных - создание всех таблиц"""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    """Получить сессию базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    """Dependency для FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
