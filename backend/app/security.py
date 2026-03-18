from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Header
import logging

from config import secret_key, algorithm

logger = logging.getLogger(__name__)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60) # 60 минут
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def verify_token(authorization: str = Header(None)):
    """Проверка токена из заголовка Authorization"""
    if not authorization:
        logger.error("No authorization header provided")
        raise HTTPException(
            status_code=401, 
            detail="Missing authorization header"
        )
    
    try:
        # Парсим "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            logger.error(f"Invalid auth scheme: {scheme}")
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        logger.info(f"Token verified for user: {payload.get('sub')}")
        return payload
    
    except ValueError:
        logger.error("Invalid authorization header format")
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(status_code=401, detail="Token verification failed")


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    if expires_delta is None:
        expires_delta = timedelta(days=25)
        
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def verify_token_optional(authorization: str = Header(None)):
    """
    Мягкая проверка токена: возвращает payload или None.
    Удобно для публичных эндпоинтов, где авторизация опциональна.
    """
    if not authorization:
        return None

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except Exception:
        return None