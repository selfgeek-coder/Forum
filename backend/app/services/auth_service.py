from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
import logging

from app.repositories.user_repository import UserRepository
from app.security import create_access_token

ph = PasswordHasher()
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, email: str, login: str, name: str, password: str):
        """Зарегистрировать нового пользователя"""

        try:
            if self.user_repository.check_email_exists(email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "USER_ALREADY_EXISTS",
                        "message": "Пользователь с такой почтой уже существует."
                    }
                )

            if self.user_repository.check_login_exists(login):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "LOGIN_ALREADY_EXISTS",
                        "message": "Этот логин уже занят."
                    }
                )

            hashed_password = ph.hash(password)

            user_id = self.user_repository.create_user(
                email, login, name, hashed_password
            )

            access_token = create_access_token(
                data={
                    "sub": email,
                    "user_id": user_id,
                    "name": login
                }
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user_id,
                "login": login,
                "email": email,
                "name": name
            }

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Register error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "REGISTER_ERROR",
                    "message": "Ошибка при регистрации пользователя."
                }
            )

    def authenticate_user(self, email: str, password: str):
        """Аутентифицировать пользователя"""

        try:
            user_data = self.user_repository.get_user_by_email(email)

            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "error": "USER_NOT_FOUND",
                        "message": "Пользователь с такой почтой не найден."
                    }
                )

            user_id, login, email, hashed_password = user_data

            try:
                ph.verify(hashed_password, password)

                if ph.check_needs_rehash(hashed_password):
                    new_hash = ph.hash(password)
                    self.user_repository.update_password(user_id, new_hash)

                access_token = create_access_token(
                    data={
                        "sub": email,
                        "user_id": user_id,
                        "name": login
                    }
                )

                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_id": user_id,
                    "login": login,
                    "email": email,
                    "name": login
                }

            except VerifyMismatchError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "error": "INVALID_PASSWORD",
                        "message": "Неверный логин или пароль."
                    }
                )

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Auth error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "AUTH_ERROR",
                    "message": "Ошибка при авторизации."
                }
            )