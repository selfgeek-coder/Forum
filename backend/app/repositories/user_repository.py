from typing import Optional, Tuple

from sqlalchemy import select
from app.db.database import SessionLocal, get_db
from app.db.models import User

class UserRepository:
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Tuple]:
        """Получить пользователя по email"""
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                return (user.id, user.login, user.email, user.password)
            return None
        finally:
            db.close()
    
    
    @staticmethod
    def check_email_exists(email: str) -> bool:
        """Проверить существование email"""

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            return user is not None
        finally:
            db.close()
    
    
    @staticmethod
    def create_user(email: str, login: str, name: str,  hashed_password: str) -> int:
        """Создать нового пользователя"""

        db = SessionLocal()
        try:
            user = User(email=email, login=login, name=name, password=hashed_password)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.id
        finally:
            db.close()