from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas import LikeCreate, LikeDelete
from app.security import verify_token
from app.repositories.like_repository import LikeRepository
from app.repositories.post_repository import PostRepository
from app.services.like_service import LikeService

router = APIRouter(prefix="/api/like", tags=["Likes API"])

like_repository = LikeRepository()
post_repository = PostRepository()
like_service = LikeService(like_repository, post_repository)


@router.post("/add")
def add_like(like: LikeCreate, current_user: dict = Depends(verify_token)):
    """Добавить лайк к посту"""
    try:
        result = like_service.add_like(current_user["user_id"], like.post_id)
        
        return {
            "success": True,
            "message": "Лайк успешно добавлен",
            "data": result
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DATABASE_ERROR",
                "message": "Ошибка базы данных при добавлении лайка"
            }
        )


@router.delete("/remove")
def remove_like(like: LikeDelete, current_user: dict = Depends(verify_token)):
    """Удалить лайк с поста"""
    try:
        result = like_service.remove_like(current_user["user_id"], like.post_id)
        
        return {
            "success": True,
            "message": "Лайк успешно удален",
            "data": result
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DATABASE_ERROR",
                "message": "Ошибка базы данных при удалении лайка"
            }
        )


@router.get("/count/{post_id}")
def get_likes_count(post_id: int):
    """Получить количество лайков на посте"""
    try:
        result = like_service.get_likes_count(post_id)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DATABASE_ERROR",
                "message": "Ошибка базы данных при получении количества лайков"
            }
        )
