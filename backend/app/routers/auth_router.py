from fastapi import APIRouter, HTTPException, status, Response, Cookie

from app.schemas import UserLogin, UserRegister
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/api", tags=["Auth API"])

# Инициализация зависимостей
user_repository = UserRepository()
auth_service = AuthService(user_repository)


@router.post("/register")
def api_register(user: UserRegister):
    try:
        result = auth_service.register_user(user.email, user.login, user.name, user.password)
        return {
            "success": True,
            "message": "Успешная регистрация.",
            "data": result
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "REGISTRATION_ERROR", "message": "Ошибка при регистрации пользователя"}
        )


@router.post("/login")
def api_login(user: UserLogin, response: Response):
    try:
        result = auth_service.authenticate_user(user.email, user.password)
        if not result:
            raise HTTPException(status_code=401, detail="Неверный email или пароль")

        user_id = result.get("user_id")
        login = result.get("login")
        if not user_id or not login:
            raise HTTPException(status_code=500, detail="Ошибка авторизации: отсутствуют данные пользователя")

        refresh_token = create_refresh_token({"user_id": user_id, "login": login})

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",
            max_age=7*24*3600
        )

        return {
            "success": True,
            "message": "Успешный вход.",
            "data": {
                "access_token": result["access_token"],
                "login": login,
                "user_id": user_id,
                "email": result.get("email"),
                "name": result.get("name"),
            }
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception("Ошибка при логине")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "LOGIN_ERROR", "message": str(e)}
        )


@router.post("/refresh")
def api_refresh(refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Отсутствует refresh token")
    try:
        payload = auth_service.verify_refresh_token(refresh_token)
        user_id = payload["user_id"]
        login = payload["login"]
        new_access_token = create_access_token({"user_id": user_id, "login": login})
        return {"access_token": new_access_token}
    except Exception:
        raise HTTPException(status_code=401, detail="Невалидный refresh token")


@router.post("/logout")
def api_logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"success": True, "message": "Вы вышли из системы"}